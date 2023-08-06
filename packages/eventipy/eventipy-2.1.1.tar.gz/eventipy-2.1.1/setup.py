# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventipy']

package_data = \
{'': ['*']}

install_requires = \
['pydantic==1.8.2']

setup_kwargs = {
    'name': 'eventipy',
    'version': '2.1.1',
    'description': 'In-memory python event library',
    'long_description': '[![Coverage Status](https://coveralls.io/repos/github/JonatanMartens/eventipy/badge.svg?branch=master)](https://coveralls.io/github/JonatanMartens/eventipy?branch=master)\n![Test eventipy](https://github.com/JonatanMartens/eventipy/workflows/test/badge.svg)\n![GitHub issues](https://img.shields.io/github/issues-raw/JonatanMartens/eventipy)\n![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/JonatanMartens/eventipy)\n![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/JonatanMartens/eventipy)\n![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/JonatanMartens/eventipy)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eventipy)\n![PyPI](https://img.shields.io/pypi/v/eventipy)\n\n\n# Eventipy\neventipy is an in-memory event library for python 3.6 and greater.\n\n## Getting Started\nTo install:\n\n`pip install eventipy`\n\nFor full documentation please visit: https://eventipy.readthedocs.io/en/stable/\n\n## Usage\n\nPublishing events:\n\n```python\nimport asyncio\nfrom eventipy import events, Event\n\nevent = Event(topic="my-topic")\nasyncio.run(events.publish(event))\n```\n\nSubscribing to topics:\n\n```python\nfrom eventipy import events, Event\n\n@events.subscribe("my-topic")\ndef event_handler(event: Event):\n    # Do something with event\n    print(event.id)\n```\n\nnow every time an event with topic `my-topic` is published, `event_handler` will be called.\n\nDefine your own events like this:\n\n```python\nclass MyEvent(Event):\n     topic = "event-topic"\n     foo: int\n     bar: int\n```\n\neventipy uses pydantic, so there is automatic type checking!\n\n## Tests\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install eventipy\n \n`pytest tests/unit`\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n\n## Versioning\nWe use [SemVer](semver.org) for versioning. For the versions available, see the tags on this repository.\n\nTo bump the version we use [`bumpversion`](https://github.com/c4urself/bump2version) to handle versions. Actions:\n\nBug fixes:\n\n```shell\n$ bumpversion patch # from v1.0.0 -> v1.0.1\n```\n\nNew features:\n\n```shell\n$ bumpversion minor # from v1.0.0 -> v1.1.0\n```\n\nBreaking changes:\n\n```shell\n$ bumpversion major # from v1.0.0 -> v2.0.0\n```\n\nThese commands will create a commit, if you want to avoid this please add the `--no-commit` flag.\n\n## License\nWe use the MIT license, see [LICENSE.md](LICENSE.md) for details\n',
    'author': 'Jonatan Martens',
    'author_email': 'jonatanmartenstav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
