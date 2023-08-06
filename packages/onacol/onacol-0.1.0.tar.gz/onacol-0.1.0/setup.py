# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onacol']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.4,<2.0.0',
 'cascadict>=0.8.4,<0.9.0',
 'ruamel.yaml>=0.17.10,<0.18.0']

setup_kwargs = {
    'name': 'onacol',
    'version': '0.1.0',
    'description': 'Oh No! Another Configuration Library',
    'long_description': None,
    'author': 'Josef Nevrly',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
