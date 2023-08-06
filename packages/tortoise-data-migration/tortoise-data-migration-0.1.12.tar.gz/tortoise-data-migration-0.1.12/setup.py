# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tortoise_data_migration']

package_data = \
{'': ['*']}

install_requires = \
['tortoise-orm>=0.17.5,<0.18.0']

setup_kwargs = {
    'name': 'tortoise-data-migration',
    'version': '0.1.12',
    'description': 'Tortoise migrations for data, not structure',
    'long_description': None,
    'author': 'Guillermo Manzato',
    'author_email': 'manzato@ekumenlabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
