# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mrmime']
install_requires = \
['Werkzeug>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'mrmime',
    'version': '0.0.1',
    'description': 'A streaming mime parser',
    'long_description': '# mrmime, a fast and memory efficient streaming MIME parser\n\nThis isn\'t API stable or even really stable at all yet. A lot of features are missing.\nYou shouldn\'t use this unless you\'re willing to actively help me with it.\n\n## Why?\n\n`email` is a memory hog, very rigid and not particularly fast. I parse a _lot_ of email\nat work and I only need a couple of things:\n - I want to control storage. I don\'t need large objects that represent the entire\n   parsed message, I need specific fields.\n - I want to control how I read up mime parts. I don\'t want massive strings.\n - I don\'t want to load the entire file into memory.\n - No serialization, only parsing.\n - I want it to be fast.\n - I want it to be intuitive.\n\n## Examples\n\nSimple example showing how to use it:\n\n```python\n\nfrom mrmime import BodyLineEvent, HeaderEvent, parse_file\n\n\nwith open("tests/data/simple.eml") as f:\n    for event in parse_file(f):\n        if isinstance(event, HeaderEvent):\n            print("header", event.key, event.value)\n        elif isinstance(event, BodyLineEvent):\n            print("line from the body", event.line)\n```\n\nHow to get the entire body in a single event:\n\n```python\n\nfrom mrmime import HeaderEvent, BodyStreamer, body_streamer, parse_file\n\nwith open("tests/data/simple.eml") as f:\n    for event in body_streamer(parse_file(f)):\n        if isinstance(event, HeaderEvent):\n            print("header", event.key, event.value)\n        elif isinstance(event, BodyStreamer):\n            print("body", event.read())\n```\n\nHow to handle multipart messages:\n\n```python\n\nfrom mrmime import ParserStateEvent, HeaderEvent, BodyLineEvent, multipart, parse_file\n\nwith open("tests/data/simple.eml") as f:\n    for event in multipart(parse_file(f)):\n        if isinstance(event, ParserStateEvent) and event.state is ParserState.Boundary:\n            print("new boundary started")\n        elif isinstance(event, HeaderEvent):\n            print("header", event.key, event.value)\n        elif isinstance(event, BodyLineEvent:\n            print("body", event.read())\n```\n\nHow to handle messages from something other than a file:\n\n```python\n\nfrom mrmime import BodyStreamer, HeaderEvent, Parser\n\nparser = Parser()\n\nfor chunk in get_data_from_source():  # e.g. an async library or something\n    for event in parser.feed(chunk):\n        if isinstance(event, HeaderEvent):\n            print("header", event.key, event.value)\n        elif isinstance(event, BodyStreamer):\n            print("body", event.read())\n```\n\n## TODO\n - Think about recursive parsing, e.g. what if I want to parse messages in messages? What if I want to decide dynamically, rather than prior?\n - MimePart should be decoding the data inside, but have the option to not do that\n - Think more about the state transitions, they\'re messy\n - we return bytes for everything at the moment, we shouldn\'t. We could make the Header object do the decoding so that it\'s lazy, that\'s a good idea.\n - Can we use memoryviews at all for the headers?\n',
    'author': 'Nathan Hoad',
    'author_email': 'nathan@hoad.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~nhoad/mrmime',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
