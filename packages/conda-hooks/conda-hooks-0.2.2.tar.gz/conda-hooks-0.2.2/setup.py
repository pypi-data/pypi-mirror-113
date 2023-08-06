# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conda_hooks']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['conda_env_store = conda_hooks.env_store:main']}

setup_kwargs = {
    'name': 'conda-hooks',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'Fabian Köhler',
    'author_email': 'fabian.koehler@protonmail.ch',
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
