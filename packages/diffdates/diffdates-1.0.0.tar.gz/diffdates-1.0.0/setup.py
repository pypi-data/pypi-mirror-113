# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diffdates']

package_data = \
{'': ['*']}

install_requires = \
['ciso8601>=2.1.3,<3.0.0']

entry_points = \
{'console_scripts': ['diffdates = diffdates.main:main']}

setup_kwargs = {
    'name': 'diffdates',
    'version': '1.0.0',
    'description': 'A command line utility to get the difference between two dates in a given input line.',
    'long_description': None,
    'author': 'Nick Rushton',
    'author_email': 'rushton.nicholas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
