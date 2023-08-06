# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pgnsplit']

package_data = \
{'': ['*']}

install_requires = \
['chess>=1.6.1,<2.0.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['pgnsplit = pgnsplit.main:main']}

setup_kwargs = {
    'name': 'pgnsplit',
    'version': '0.1.1',
    'description': 'Simple package that splits a chess pgn file into a folder of pgns - each one containing one variation of the original pgn.',
    'long_description': None,
    'author': 'vsingh18567',
    'author_email': '59497793+vsingh18567@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
