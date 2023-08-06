# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vidoptim', 'vidoptim.schemas']

package_data = \
{'': ['*']}

install_requires = \
['click-spinner>=0.1.10,<0.2.0',
 'colorama>=0.4.4,<0.5.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'gevent>=21.1.2,<22.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.61.1,<5.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['vidoptim = vidoptim:cli']}

setup_kwargs = {
    'name': 'vidoptim',
    'version': '0.0.1a4',
    'description': 'ffmpeg backed video optimizer',
    'long_description': '# vidoptim\n\n`ffmpeg` backed video optimization tool.\n',
    'author': 'Nik Cubrilovic',
    'author_email': 'git@nikcub.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nc9/vidoptim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
