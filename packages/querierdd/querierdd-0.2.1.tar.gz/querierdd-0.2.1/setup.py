# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['querierdd']
install_requires = \
['click>=8.0.1,<9.0.0', 'psutil>=5.8.0,<6.0.0']

entry_points = \
{'console_scripts': ['querier = querierdd:cli']}

setup_kwargs = {
    'name': 'querierdd',
    'version': '0.2.1',
    'description': 'Query the system and present details in an asthetically pleasing way.',
    'long_description': None,
    'author': 'egee-irl',
    'author_email': 'brian@egee.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
