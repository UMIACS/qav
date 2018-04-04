# Question Answer Validation (qav)

[![pypi version](https://img.shields.io/pypi/v/qav.svg)](https://pypi.python.org/pypi/qav)
[![license](https://img.shields.io/pypi/l/qav.svg)](https://pypi.python.org/pypi/qav)
[![pyversions](https://img.shields.io/pypi/pyversions/qav.svg)](https://pypi.python.org/pypi/qav)
[![pipeline status](https://gitlab.umiacs.umd.edu/staff/qav/badges/master/pipeline.svg)](https://gitlab.umiacs.umd.edu/staff/qav/commits/master)
[![coverage report](https://gitlab.umiacs.umd.edu/staff/qav/badges/master/coverage.svg)](https://gitlab.umiacs.umd.edu/staff/qav/commits/master)

qav is a Python library for console-based question and answering, with the
ability to validate input.

It provides question sets to group related questions.  Questions can also
have subordinate Questions underneath them.  Answers to those questions can be
validated based on a simple, static piece of information provided by you.
Answers may also be validated dynamically based on the information provided in
previous questions.

## Example Usage
```
>>> from qav.questions import Question
>>> from qav.validators import ListValidator
>>> q = Question('How old am I? ', 'age', ListValidator(['20', '35', '40']))
>>> q.ask()
Please select from the following choices:
 [0] - 20
 [1] - 35
 [2] - 40
How old am I? : 0
>>> q.answer()
# returns => {'age': '20'}
```

## Requirements
`netaddr`

## Installation
```
$ pip install qav
```

## Compatibility
This library has been tested to support:
* Python26
* Python27
* Python36

## License

    qav - question answer validation in Python
    Copyright (C) 2015  UMIACS

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

    Email:
        github@umiacs.umd.edu
