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
    'version': '3.0.1',
    'description': 'Generate QR cards for any occasion',
    'long_description': '# wifi_qrcode\n\nGenerate WiFi Access QR Codes\n\n# Installation\n\n```bash\npip install makeqr\n```\n\n# Usage example\n\nTo test that installation was successful, try:\n\n```bash\nmakeqr wifi --help\n```\n\nUsage from the command line:\n\n```bash\nmakeqr wifi --ssid MYWIRELESSNETWORK --auth WPA --password SECRET\n```\n\n... or as python module:\n\n```bash\npython -m makeqr wifi --ssid MYWIRELESSNETWORK --auth WPA --password SECRET\npython -m makeqr mailto --to user@mail.org --subject "Mail from QR"\n```\n\n# Features\n\n- [x] geo\n- [x] link\n- [x] mailto\n- [x] sms\n- [x] tel\n- [x] wifi\n',
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
