# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['iytdl', 'iytdl.types']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0',
 'Pyrogram>=1.2.9,<2.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'hachoir>=3.1.2,<4.0.0',
 'html-telegraph-poster>=0.4.0,<0.5.0',
 'mutagen>=1.45.1,<2.0.0',
 'youtube-search-python==1.4.6',
 'youtube_dl>=2021.6.6,<2022.0.0']

setup_kwargs = {
    'name': 'iytdl',
    'version': '0.2.5',
    'description': 'Asynchronous Standalone Inline YouTube-DL Module',
    'long_description': '# iytdl\n\nAsynchronous Standalone Inline YouTube-DL Module\n',
    'author': 'Leorio Paradinight',
    'author_email': '62891774+code-rgb@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iytdl/iytdl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
