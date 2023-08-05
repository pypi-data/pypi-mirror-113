# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typetest']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.18.1,<2.0.0']

setup_kwargs = {
    'name': 'typetest',
    'version': '0.1.0',
    'description': 'Test your typing speed without leaving the terminal.',
    'long_description': None,
    'author': 'MasterMedo',
    'author_email': 'mislav.vuletic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
