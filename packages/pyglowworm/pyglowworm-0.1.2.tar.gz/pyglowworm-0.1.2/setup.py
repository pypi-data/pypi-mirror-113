# encoding: utf-8
"""
@file: setup.py
@desc:
@author: zhenguo
@time: 2021/7/19
"""

# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="pyglowworm",
    version="0.1.2",
    author="zhenguo",
    author_email="guozhennianhua@163.com",
    description="to assist finding examples for api of all kinds of libraries",
    long_description=open("README.md").read(),
    license="MIT",
    url="https://github.com/jackzhenguo/python-small-examples",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
