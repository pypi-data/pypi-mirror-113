# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toml_adapt', 'toml_adapt.tests']

package_data = \
{'': ['*'], 'toml_adapt.tests': ['data/*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['toml-adapt = toml_adapt.main:start']}

setup_kwargs = {
    'name': 'toml-adapt',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'iztokf',
    'author_email': 'iztokf@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
