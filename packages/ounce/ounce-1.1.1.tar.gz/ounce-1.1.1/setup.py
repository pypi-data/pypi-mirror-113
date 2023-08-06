# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ounce']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ounce',
    'version': '1.1.1',
    'description': 'Fast, simple, non-fancy, and non-magical package for manipulating units of measure',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ounce.readthedocs.io/en/stable/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
