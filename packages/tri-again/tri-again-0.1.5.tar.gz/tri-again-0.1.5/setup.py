# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tri_again']

package_data = \
{'': ['*']}

install_requires = \
['numpy',
 'polliwog==1.0.0b14',
 'pycollada>=0.7.1,<0.8',
 'toolz>=0.10.0,<0.12.0',
 'vg>=1.11.1',
 'webcolors>=1.11.1,<2']

setup_kwargs = {
    'name': 'tri-again',
    'version': '0.1.5',
    'description': 'Work with polygonal meshes which have vertex-wise correspondence',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lace/entente',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
