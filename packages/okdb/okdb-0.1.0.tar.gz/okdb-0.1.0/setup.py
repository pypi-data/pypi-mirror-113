# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['okdb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'okdb',
    'version': '0.1.0',
    'description': 'Simple database with which I am productive',
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
