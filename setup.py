# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""metaweather api"""

from setuptools import setup, find_packages

setup(
    name='meta',
    version='0.1.0',
    include_package_data=True,
    install_requires=['asyncpg==0.18.3', 'aiohttp==3.3.2',
                      'uvloop==0.12.0', 'requests==2.20.1',
                      'trafaret-config==2.0.2'],
    setup_requires=['pytest-runner', 'pytest', 'pytest-pylint'],
    tests_require=['pytest', 'pytest-asyncio', 'pytest-aiohttp', 'pytest-cov',
                   'pylint'],
    packages=find_packages(),
)
