#!/usr/bin/env python
# coding: utf-8

# In[1]:

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'fake_vn_user',
    version = '1.0.1',
    description = 'A library use for fake user in VN, created by NeV3RmI, visit my website: https://picks.work',
    py_module = ['fake_vn_user'],
    package_dir = {'':'src'},
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nev3rmi/fake_vn_user",
    author="NeV3RmI",
    author_email="admin@picks.work",
)

