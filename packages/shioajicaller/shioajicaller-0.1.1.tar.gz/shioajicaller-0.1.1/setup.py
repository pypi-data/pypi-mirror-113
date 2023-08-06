# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shioajicaller', 'shioajicaller.cli', 'shioajicaller.codes']

package_data = \
{'': ['*']}

install_requires = \
['dotenv>=0.0.5,<0.0.6', 'shioaji>=0.3.2.dev4,<0.4.0']

setup_kwargs = {
    'name': 'shioajicaller',
    'version': '0.1.1',
    'description': 'shioaj warp caller',
    'long_description': None,
    'author': 'Steve Lo',
    'author_email': 'info@sd.idv.tw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
