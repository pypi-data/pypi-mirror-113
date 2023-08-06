# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scuzzie']

package_data = \
{'': ['*']}

install_requires = \
['Mako>=1.1.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'marshmallow>=3.10.0,<4.0.0',
 'python-slugify>=4.0.1,<5.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['scuzzie = scuzzie.cli:scuzzie']}

setup_kwargs = {
    'name': 'scuzzie',
    'version': '0.1.0',
    'description': 'Simple static webcomic site generator.',
    'long_description': None,
    'author': 'backwardspy',
    'author_email': 'backwardspy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
