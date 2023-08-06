# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makeqr', 'makeqr.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic[email]>=1.8.2,<2.0.0',
 'qrcode[pil]>=7.1,<8.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['makeqr = makeqr.app:main']}

setup_kwargs = {
    'name': 'makeqr',
    'version': '3.0.0',
    'description': 'Generate QR cards for any occasion',
    'long_description': None,
    'author': 'Aleksandr Shpak',
    'author_email': 'shpaker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shpaker/makeqr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
