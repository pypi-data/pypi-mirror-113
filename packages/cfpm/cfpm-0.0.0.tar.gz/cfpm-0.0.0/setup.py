# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfpm']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click-log>=0.3.2,<0.4.0',
 'click>=8.0.1,<9.0.0',
 'semver>=2.13.0,<3.0.0',
 'tomli>=1.0.4,<2.0.0']

entry_points = \
{'console_scripts': ['cfpm = cfpm.console:cli']}

setup_kwargs = {
    'name': 'cfpm',
    'version': '0.0.0',
    'description': 'The C-Family Package Manager.',
    'long_description': None,
    'author': 'Yi Cao',
    'author_email': 'caoyi06@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/project-cfpm/cfpm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
