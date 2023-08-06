from __future__ import annotations

import base64
import dataclasses
import enum
import functools
import quopri
import sys
import werkzeug.http
from io import BytesIO
from typing import TYPE_CHECKING, Iterator, IO, Union, cast


if TYPE_CHECKING:
    Event = Union[
        "HeaderEvent",
        "ContentTypeHeaderEvent",
        "MalformedHeaderEvent",
        "BodyLineEvent",
        "ParserStateEvent",
        "BodyStreamer",
    ]


class Flags:
    """Private object for indicating additional parser state."""

    content_transfer_encoding: bytes | None = None
    content_type: bytes | None = None
    multipart: bool = False
    boundary: bytes | None = None
    charset: bytes | None = None

    def __repr__(self) -> str:
        return (
            "Flags<"
            f"content_transfer_encoding={repr(self.content_transfer_encoding)}|"
            f"content_type={repr(self.content_type)}|"
            f"multipart={repr(self.multipart)}|"
            f"boundary={repr(self.boundary)}"
            f"charset={repr(self.charset)}"
            ">"
        )


class ParserState(enum.Enum):
    NotStarted = enum.auto()
    HeaderStart = enum.auto()
    HeaderComplete = enum.auto()
    MimeStart = enum.auto()
    MimeBoundary = enum.auto()
    MimeInProgress = enum.auto()
    MimeEnd = enum.auto()


@dataclasses.dataclass
class HeaderEvent:
    key: bytes
    value: bytes


class ContentTypeHeaderEvent(HeaderEvent):
    @functools.cached_property
    def content_type(self) -> bytes:
        return self.value.split(b";")[0].lower()

    @functools.cached_property
    def is_multipart(self) -> bool:
        return self.content_type.startswith(b"multipart/")

    @functools.cached_property
    def args(self) -> dict[str, str]:
        args = self.value.split(b";")
        if len(args) == 1:
            return {}
        # FIXME: this is a huge dependency just for this.
        v = werkzeug.http.parse_dict_header(args[1].strip().decode("ascii"))
        return v

    @functools.cached_property
    def boundary(self) -> bytes:
        if not self.is_multipart:
            raise ValueError("Not a multipart content-type header")
        return self.args["boundary"].encode("ascii")

    @functools.cached_property
    def charset(self) -> bytes | None:
        if "charset" in self.args:
            return self.args["charset"].encode("ascii")
        return None


@dataclasses.dataclass
class MalformedHeaderEvent:
    line: bytes


@dataclasses.dataclass
class BodyLineEvent:
    line: bytes


@dataclasses.dataclass
class ParserStateEvent:
    state: ParserState


@dataclasses.dataclass
class Parser:
    # buf is a list of physical lines. list instead of BytesIO to avoid reparsing for
    # line endings constantly
    buf: list[bytes] = dataclasses.field(default_factory=list)
    flags: Flags = dataclasses.field(default_factory=Flags)
    state: ParserState = ParserState.NotStarted
    current_header: list[bytes] = dataclasses.field(default_factory=list)

    def write_chunk(self, chunk: bytes) -> bool:
        """Write the given chunk to our buffer, mending lines where necessary."""

        lines = chunk.splitlines(keepends=True)
        # smash that line back together
        if self.buf and self.buf[-1][-1] != b"\n"[0]:
            self.buf[-1] += lines.pop(0)
        self.buf.extend(lines)
        return self.buf[-1][-1] == 10

    def feed(self, chunk: bytes) -> Iterator[Event]:
        """
        Feed the given chunk to the parser, and return a generator for all the events.

        Note that you _must_ consume the events, you cannot let them accumulate.
        """
        if not self.write_chunk(chunk):
            # we don't have any complete lines, no point parsing yet
            return

        state = self.state
        flags = self.flags

        while self.buf:
            line = self.buf.pop(0)
            # we're on our final line
            if not self.buf:
                # it's not a complete read
                if line[-1] != b"\n"[0]:
                    # shove it back in the buffer for processing next time
                    self.buf[:] = [line]
                    break

            if state == ParserState.NotStarted:
                state = ParserState.HeaderStart
                self.current_header.append(
                    line.removesuffix(b"\r\n").removesuffix(b"\n").lstrip()
                )
            elif state == ParserState.HeaderStart:
                # line continuation, keep reading lines until we have the start of the
                # next thing
                if line[0] in b" \t":
                    self.current_header.append(
                        line.removesuffix(b"\r\n").removesuffix(b"\n").lstrip()
                    )
                    continue

                # if we're here, then current_header is complete and we should
                complete_line = b" ".join(self.current_header)
                # every line except the last one forms a complete header
                self.current_header[:] = [
                    line.removesuffix(b"\r\n").removesuffix(b"\n").lstrip()
                ]

                # FIXME: not a given, I think? X-MS-Journal-Report: in journal_email.eml
                # for example
                if b": " not in complete_line:
                    yield MalformedHeaderEvent(complete_line)
                else:
                    key, value = complete_line.split(b": ", 1)

                    header = HEADER_REGISTRY.get(key.lower(), HeaderEvent)(key, value)

                    if key.lower() == b"content-transfer-encoding":
                        flags.content_transfer_encoding = value.lower()
                    elif isinstance(header, ContentTypeHeaderEvent):
                        flags.multipart = header.is_multipart
                        if flags.multipart:
                            flags.boundary = header.boundary
                        flags.content_type = header.content_type
                        flags.charset = header.charset

                    yield header

                if line in {b"\r\n", b"\n"}:
                    # headers are done, just reset the buffer. We don't care about the
                    # new lines.
                    self.current_header.clear()
                    yield ParserStateEvent(ParserState.HeaderComplete)
                    state = ParserState.MimeStart
                else:
                    # new header has started
                    state = ParserState.HeaderStart
            elif flags.multipart:
                if state == ParserState.MimeStart:
                    boundary = line.strip()
                    if flags.boundary is None or b"--" + flags.boundary != boundary:
                        raise ValueError(
                            "was expecting boundary", flags.boundary, boundary
                        )

                    state = ParserState.MimeBoundary
                    yield ParserStateEvent(state)
                elif state == ParserState.MimeBoundary:
                    if line.strip() == b"--" + cast(bytes, flags.boundary):
                        yield ParserStateEvent(ParserState.MimeBoundary)
                    elif line.strip() == b"--" + cast(bytes, flags.boundary) + b"--":
                        state = ParserState.MimeEnd
                        yield ParserStateEvent(state)
                    else:
                        yield BodyLineEvent(line)
                elif state == ParserState.MimeEnd:
                    raise ValueError(
                        "Data after we've finished our mime content??", line
                    )
            elif state == ParserState.MimeStart:
                state = ParserState.MimeInProgress
                yield BodyLineEvent(decode_line(flags.content_transfer_encoding, line))
            elif state == ParserState.MimeInProgress:
                yield BodyLineEvent(decode_line(flags.content_transfer_encoding, line))

        self.state = state
        self.flags = flags


def multipart(events: Iterator[Event]) -> Iterator[Event]:
    parser: Parser

    for event in events:
        if (
            isinstance(event, ParserStateEvent)
            and event.state is ParserState.MimeBoundary
        ):
            parser = Parser()
            yield event
        elif isinstance(event, BodyLineEvent):
            for event in parser.feed(event.line):
                yield event
        else:
            yield event


def body_streamer(events: Iterator[Event]) -> Iterator[Event]:
    """
    Take the events iterator and turn collections of Body events into a file-like
    object.
    """
    for event in events:
        if not isinstance(event, BodyLineEvent):
            yield event
        else:
            body = BodyStreamer(event.line, events)
            yield body

            # if the consumer didn't read the entire body up, then just consume it for
            # them
            if body.last_event is None:
                # readline instead of read to minimize memory impact
                while body.readline():
                    pass

            # the body knows it's complete when it gets a non-Body event, so we need
            # to make sure we yield that.
            if body.last_event is not None:
                yield body.last_event


@dataclasses.dataclass
class BodyStreamer:
    """
    A vaguely file like object for presenting MIME bodies as files.

    Not seekable or tellable.
    """

    first: bytes | None
    events: Iterator[Event]
    last_event: Event | None = None

    def read(self, size: int = -1) -> bytes:
        """
        Read from the given stream.

        If you specify a read size, the returned result will be approximate, i.e. it
        may be more than you asked for.
        """
        if size == 0:
            raise ValueError("read size of 0 doesn't make sense")
        elif size == -1:
            return b"".join(self)
        else:
            buf = BytesIO()
            while buf.tell() < size:
                if not (line := self.readline()):
                    break
                else:
                    buf.write(line)
            return buf.getvalue()

        if size != -1:
            assert False

    def readline(self) -> bytes:
        """Return a single line."""
        if self.first is not None:
            first, self.first = self.first, None
            return first
        if self.last_event is not None:
            return b""

        try:
            event = next(self.events)
        except StopIteration:
            return b""
        else:
            if not isinstance(event, BodyLineEvent):
                self.last_event = event
                raise StopIteration
            else:
                return event.line

    def __iter__(self) -> Iterator[bytes]:
        return self

    def __next__(self) -> bytes:
        if not (line := self.readline()):
            raise StopIteration
        return line


def decode_line(content_transfer_encoding: bytes | None, line: bytes) -> bytes:
    if content_transfer_encoding is None or not line.strip():
        return line
    if content_transfer_encoding == b"quoted-printable":
        line = quopri.decodestring(line)
    elif content_transfer_encoding == b"base64":
        line = base64.decodebytes(line)
    return line


HEADER_REGISTRY = {
    b"content-type": ContentTypeHeaderEvent,
}


def parse_file(stream: IO[bytes], buf_size: int = 4096) -> Iterator[Event]:
    parser = Parser()

    # FIXME: read_into maybe?
    while b := stream.read(buf_size):
        yield from parser.feed(b)


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        for event in parse_file(f):
            if isinstance(event, BodyLineEvent):
                print("body", event.line)
            elif isinstance(event, HeaderEvent):
                print("header", event.key, event.value)
            else:
                print("event", event)
