# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hobart']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'polliwog==1.0.0b14', 'scipy', 'vg>=1.11.1']

setup_kwargs = {
    'name': 'hobart',
    'version': '1.0.0b3',
    'description': 'Obtain cross sections of polygonal meshes',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hobart.readthedocs.io/en/stable/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
