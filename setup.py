#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import ast
from setuptools import find_packages, setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('revision/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))

setup(
    name='revision',
    version=version,
    description='Static assets revisioning library.',
    author='SENSY Inc.',
    url='https://github.com/COLORFULBOARD/revision',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'click==6.7',
        'requests==2.18.4',
        'six==1.11.0',
    ],
    extras_require={
        'dev': [
            'flake8==3.4.1',
            'pytest==3.2.2',
            'tox==2.9.1',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={'console_scripts': [
        'revision=revision.cli:main'
    ]}
)
