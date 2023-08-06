# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teppan']

package_data = \
{'': ['*']}

install_requires = \
['shioaji>=0.3.2.dev4,<0.4.0']

setup_kwargs = {
    'name': 'teppan',
    'version': '0.2a1',
    'description': 'Teppan is integrated for Sinopac Trading API - Shioaji.',
    'long_description': None,
    'author': 'yp0chien',
    'author_email': 'ypochien@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
