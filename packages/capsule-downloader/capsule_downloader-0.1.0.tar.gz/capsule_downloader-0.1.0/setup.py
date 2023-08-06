# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['capsule_downloader']
install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'lxml>=4.6.3,<5.0.0',
 'requests>=2.26.0,<3.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['capsule_downloader = capsule_downloader:main']}

setup_kwargs = {
    'name': 'capsule-downloader',
    'version': '0.1.0',
    'description': 'A tool to help users easily download capsules from aotu.ai',
    'long_description': None,
    'author': 'Stephen Li',
    'author_email': 'stephen@aotu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.6.2,<4.0',
}


setup(**setup_kwargs)
