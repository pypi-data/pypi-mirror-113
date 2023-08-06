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
    'version': '0.1.2',
    'description': 'Simple package that splits a chess pgn file into a folder of pgns - each one containing one variation of the original pgn.',
    'long_description': "# pgnsplit\n\n`pgnsplit` is a simple command-line application that takes a single [pgn](https://en.wikipedia.org/wiki/Portable_Game_Notation) file (e.g. from a [Lichess Study](https://lichess.org/study/KjivNw7F)) and extracts all the variations in the pgn, putting each of them in their own individual pgn files in a folder `./pgn/`, which can then be stored in some sort of database (e.g. in SCID or ChessX).\n\nThis solves the problem in various chess software, where importing pgns only stores the mainline variation. \n\nThis is presented as a lightweight and easy-to-use alternative to [David J. Barnes' pgn-extract](https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/help.html), which is still more appropriate for the intricate manipulation of pgn files. \n\n## Requirements\n* Python (>3.8)\n* pip (which normally comes with Python)\n\n## Installation\n```bash\n$ pip install pgnsplit\n```\n\n## Usage\n```bash\n$ pgnsplit <filepath>\n```\n`<filepath>` must be the path to a properly formatted pgn file. The individual pgn files will be stored in a local folder. \n\n## Improvements\nFurther improvements/functionality could be made as requested/needed.",
    'author': 'vsingh18567',
    'author_email': 'vsingh18567@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vsingh18567/pgn-split',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
