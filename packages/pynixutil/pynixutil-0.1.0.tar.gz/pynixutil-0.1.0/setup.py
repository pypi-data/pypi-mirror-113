# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynixutil']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'pynixutil',
    'version': '0.1.0',
    'description': 'Utility functions for working with Nix in Python',
    'long_description': None,
    'author': 'adisbladis',
    'author_email': 'adam.hose@tweag.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tweag/pynixutil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
