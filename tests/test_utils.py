# -*- coding: utf-8 -*-

from qav.utils import bold


def test_bold():
    assert bold('foo') == '\x1b[1mfoo\x1b[0m'
