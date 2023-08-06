# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optimap']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.2,<5.0',
 'matplotlib>=3.2,<4.0',
 'numpy>=1.19,<2.0',
 'scikit-image>=0.16,<0.17']

setup_kwargs = {
    'name': 'optimap',
    'version': '0.1.0',
    'description': 'Optimized integrated intensity map method for spectral cubes',
    'long_description': '# optimap\nOptimized integrated intensity map method for spectral cubes\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/optimap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
