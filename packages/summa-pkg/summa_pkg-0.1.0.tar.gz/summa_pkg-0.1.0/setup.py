# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['summa_pkg']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'summa-pkg',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'romansnetkov',
    'author_email': 'snetkov.roman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
