#!/usr/bin/env python

try:
    from setuptools import setup
    extra = dict(test_suite="tests.test.suite", include_package_data=True)
except ImportError:
    from distutils.core import setup
    extra = {}

long_description = \
'''
qav is a Python library for console-based question and answering, with the
ability to validate input.
'''

from qav import __version__

setup(
    name='qav',
    version=__version__,
    author='Derek Yarnell',
    author_email='derek@umiacs.umd.edu',
    packages=['qav'],
    install_requires=[
        'netaddr',
    ],
    url='https://github.com/UMIACS/qav',
    license='LGPL v2.1',
    description='Question Answer Validation',
    long_description=long_description,
    **extra
)
