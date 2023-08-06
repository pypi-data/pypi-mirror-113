# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sourcery']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-sourcery',
    'version': '0.0.0',
    'description': 'Various extractors that generate a SQLite database (with tricks)',
    'long_description': None,
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
