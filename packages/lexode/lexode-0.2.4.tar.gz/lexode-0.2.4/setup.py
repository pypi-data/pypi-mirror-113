# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lexode']
setup_kwargs = {
    'name': 'lexode',
    'version': '0.2.4',
    'description': 'Lexicographic packing and unpacking',
    'long_description': '# python-lexode\n\nlexicographic packing and unpacking functions for ordered key-value stores\n\n![Funny bunny in front of brick of wall](https://images.unsplash.com/photo-1584759985030-352927f481a3?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max&ixid=eyJhcHBfaWQiOjEyMDd9)\n',
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
