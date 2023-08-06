# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ezstore']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.4.7,<4.0.0']

setup_kwargs = {
    'name': 'ezstore',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Roni Sundstrom',
    'author_email': 'ronttipontti.sundstrom2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
