# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skunkbooth', 'skunkbooth.data', 'skunkbooth.filters', 'skunkbooth.utils']

package_data = \
{'': ['*']}

install_requires = \
['asciimatics>=1.13,<2.0', 'opencv-python>=4.5,<5.0']

entry_points = \
{'console_scripts': ['skunkbooth = skunkbooth.main:main']}

setup_kwargs = {
    'name': 'skunkbooth',
    'version': '0.1.1',
    'description': 'A camera app in terminal. One more reason to stay inside terminal.',
    'long_description': '- [Skunkbooth](#skunkbooth)\n- [Usage](#usage)\n    - [Installation](#installation)\n    - [Run](#run)\n    - [Media location](#media-location)\n- [Contributing](#contributing)\n    - [Install Poetry](#install-poetry)\n    - [Clone the repo](#clone-the-repo)\n    - [Activate poetry shell](#activate-poetry-shell)\n    - [Install dev deps](#install-dev-deps)\n    - [Run the application](#run-the-application)\n    - [Logs](#logs)\n# Skunkbooth\n\nA camera app in terminal. One more reason to stay inside terminal.\n\n# Usage\n### Installation\n```shell\npip install skunkbooth\n```\n\n### Run\nAfter installation, use `skunkbooth` command to launch camera.\n\n```shell\nskunkbooth\n```\n### Media location\n\n- macOS and Linux\n```shell\nls ~/skunkbooth/pictures\n```\n\n- Windows\n```powershell\ndir C:\\Users\\<username>\\skunkbooth\\pictures\n```\n\n# Contributing\n[Poetry](https://python-poetry.org/) is used for package management.\n\n### Install Poetry\n\n- macOS, Linux or WSL\n```shell\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -\n```\n\n- Windows Powershell\n```shell\n(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -\n```\n\n### Clone the repo\n```shell\ngit clone https://github.com/Davidy22/scholarlySkunkJam.git\ncd scholarlySkunkJam\n```\n### Activate poetry shell\n```shell\npoetry shell\n```\n\n### Install dev deps\n```shell\npoetry install\n```\n\n### Run the application\n```shell\npython3 -m skunkbooth.main\n```\n\n### Logs\nLogs are located in `skunkbooth` folder.\n- macOS and Linux\n```shell\nls ~/skunkbooth/.logs\n```\n\n- Windows\n```powershell\ndir C:\\Users\\<username>\\skunkbooth\\.logs\n```\n',
    'author': 'Davidy22, dhananjaylatkar, Trisanu-007, shriram1998 and garuna-m6',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Davidy22/scholarlySkunkJam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
