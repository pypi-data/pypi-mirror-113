# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['deviant']
setup_kwargs = {
    'name': 'deviant',
    'version': '0.0.8',
    'description': 'Модуль для работки с Deviant Api',
    'long_description': None,
    'author': 'Deviant',
    'author_email': 'darsox.anime@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
