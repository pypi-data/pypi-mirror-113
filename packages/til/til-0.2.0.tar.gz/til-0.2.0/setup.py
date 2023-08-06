# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['til', 'til.plugins']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'ruamel.yaml>=0.17.4,<0.18.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['til = til.main:til']}

setup_kwargs = {
    'name': 'til',
    'version': '0.2.0',
    'description': 'Keep track of things you learn each day',
    'long_description': '\nCLI tool for recording and tracking things you learn(TILs).\n\n## Demo\n\n<img src="./assets/demo.gif"/>\n\n## Install TIL\n```bash\n$ pip install til-cli\n```\n\nThen start adding things that you learn:\n```bash\n$ til new "How to parse yaml in Python"\nContent:\nJust use ruamel.yaml\npip install ruamel.yaml\n^C\n```\n\nStore your TILs wherever you want using TIL plugins:\n- YAML: Write to a yaml file\n- ...more to come...\n\nCopy `.til.toml.default` to your home directory as `.til.toml` and add more plugins or change their configuration.\nAs an example by default TIL uses YAML plugin to store entries in `til.yaml` file in your home directory, this is configurable.\n\n[Simon Willison\'s TIL Page](https://til.simonwillison.net/) was main inspiration to be able to create something similar with minimal extra effort.\n\nPlanned features:\n- [x] Initial implementation\n- [x] YAML plugin as POC\n- [ ] CI / CD for publishing to pypi with releases\n- [ ] some tests\n- [ ] Other tools to install\n    - [ ] MacOS - brew\n    - [ ] Debian/Ubuntu - apt (snap packages?)\n- [ ] More plugins\n    - [ ] POST to endpoint\n    - [ ] Twitter\n    - [ ] Email?\n- [ ] tags support (e.g. Python, js, k8s, devops, science, etc.)\n- [ ] Search tils by\n    - [ ] keyword\n    - [ ] tags\n\n\n## Contribute:\n#### Install Python 3.x\nRequires Python >= 3.9.\n\nConsider installing it either with brew or using a tool like [pyenv](https://github.com/pyenv/pyenv)\n\n##### Macos\n```bash\n$ brew install python@3.9\n```\n\nOr download from [Python.org](https://www.python.org/downloads/)\n\n#### Install poetry\n```bash\n$ brew install poetry\n\n```\nor\n\n```bash\n$ pip3 install poetry\n```\n\n#### Create Env\n```bash\n$ poetry env use python3.9          # Setup env\n$ poetry shell                      # Drop into Poetry env\n$ poetry install                    # Install from pyproject.toml\n```\n\n',
    'author': 'Kamyar Ghasemlou',
    'author_email': 'github@kamy.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kamyar/til',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
