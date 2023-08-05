# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['strictify']
setup_kwargs = {
    'name': 'strictify',
    'version': '0.1.0',
    'description': 'A strict decorator for python',
    'long_description': None,
    'author': 'Mikhail',
    'author_email': 'joinmma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
