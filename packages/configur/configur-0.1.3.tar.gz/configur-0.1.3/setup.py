# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configur']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.18.4,<2.0.0',
 'python-box>=5.3.0,<6.0.0',
 'python-dotenv>=0.18.0,<0.19.0',
 'tomlkit>=0.7.2,<0.8.0']

setup_kwargs = {
    'name': 'configur',
    'version': '0.1.3',
    'description': 'TOML-based configuration for Python',
    'long_description': None,
    'author': 'Ryan Whitten',
    'author_email': 'rw@heyrw.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
