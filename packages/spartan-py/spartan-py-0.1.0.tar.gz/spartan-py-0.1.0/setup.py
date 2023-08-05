# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spartan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spartan-py',
    'version': '0.1.0',
    'description': 'Library for spartan protocol',
    'long_description': None,
    'author': 'Hedy Li',
    'author_email': 'hedy@tilde.cafe',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
