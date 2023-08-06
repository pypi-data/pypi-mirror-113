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
    'version': '2.1.0',
    'description': 'In-memory python event library',
    'long_description': None,
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
