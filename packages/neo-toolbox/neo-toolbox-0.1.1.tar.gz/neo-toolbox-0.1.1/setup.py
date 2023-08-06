# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neo_toolbox']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'neo-toolbox',
    'version': '0.1.1',
    'description': 'Tools for working with the Neo N3 blockchain.',
    'long_description': None,
    'author': 'Adrian Fjellberg',
    'author_email': 'adrian@adapted.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
