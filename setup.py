#!/usr/bin/python3
# Copyright (c) 2015 Your Name
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from setuptools import find_packages
from setuptools import setup

setup(name='forvm',
	version='0.1',
	description='forvm dapp library',
	author='Empty Author',
	author_email='forvm@gmail.com',
	setup_requires='setuptools',
	package_dir={'':'library'},
	packages=['forvm']
)
