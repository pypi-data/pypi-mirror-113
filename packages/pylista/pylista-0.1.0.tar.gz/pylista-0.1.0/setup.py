# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylista']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['pylista = pylista.cli:cli']}

setup_kwargs = {
    'name': 'pylista',
    'version': '0.1.0',
    'description': 'A simple CLI tool to manage lists',
    'long_description': None,
    'author': 'Herson Oliveira',
    'author_email': 'oliveira.herson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
