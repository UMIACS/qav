#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],
    url='https://github.com/UMIACS/qav',
    license='LGPL v2.1',
    description='Question Answer Validation',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],

)
