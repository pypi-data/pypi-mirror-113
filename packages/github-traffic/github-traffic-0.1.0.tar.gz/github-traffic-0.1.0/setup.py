# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['github_traffic']
install_requires = \
['PyGithub>=1.43.8',
 'click-aliases>=1.0.1,<2.0.0',
 'click>=7',
 'terminaltables>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['github-traffic = github_traffic:cli']}

setup_kwargs = {
    'name': 'github-traffic',
    'version': '0.1.0',
    'description': 'Summarize Github traffic stats across repositories.',
    'long_description': None,
    'author': 'Jashandeep Sohi',
    'author_email': 'jashandeep.s.sohi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
