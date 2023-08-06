# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sn_demo']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['sn-demo = sn_demo.main:app']}

setup_kwargs = {
    'name': 'sn-demo',
    'version': '0.3.0',
    'description': '',
    'long_description': '',
    'author': 'Rick Sanchez',
    'author_email': 'rick@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
