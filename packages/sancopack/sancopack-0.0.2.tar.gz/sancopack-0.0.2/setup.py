#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='sancopack',
    version='0.0.2',
    author='sanco',
    author_email='sanco1987@gmail.com',
    url='https://www.winrobot360.com',
    description=u'collect packages',
    packages=['sancopack'],
    install_requires=['requests', 'pipdeptree'],
)