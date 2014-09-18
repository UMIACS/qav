#!/usr/bin/env python

try:
    from setuptools import setup
    extra = dict(test_suite="tests.test.suite", include_package_data=True)
except ImportError:
    from distutils.core import setup
    extra = {}

long_description = \
'''
A python library for console-based raw input-based questions with answers and
extensive and extensible validation for answers.
'''


setup(
    name='qav',
    version='0.1.0',
    author='Derek Yarnell',
    author_email='derek@umiacs.umd.edu',
    packages=['qav'],
    url='',
    license='LICENSE.txt',
    description='Question Answer Validation',
    long_description=long_description,
    **extra
)
