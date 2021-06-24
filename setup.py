#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='attractors',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'attractors = src.parser:cli',
        ],
    },
)