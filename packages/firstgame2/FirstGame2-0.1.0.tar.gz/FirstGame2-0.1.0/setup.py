# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firstgame2']

package_data = \
{'': ['*']}

install_requires = \
['keyboard>=0.13.5,<0.14.0', 'matplotlib>=3.4.2,<4.0.0', 'numpy>=1.21.1,<2.0.0']

setup_kwargs = {
    'name': 'firstgame2',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'gregdavies91',
    'author_email': 'greg@facetothelight.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
