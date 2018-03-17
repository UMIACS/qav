# -*- coding: utf-8 -*-

from qav.listpack import ListPack


class TestListPack(object):

    def test_defaults(self):
        deets = [('name', 'Cicero'), ('occupation', 'orator')]
        lp = ListPack(deets)
        assert str(lp) == '\n\x1b[1mname\x1b[0m: Cicero  \x1b[1moccupation\x1b[0m: orator  '

    def test_non_defaults(self):
        deets = [('name', 'Cicero'), ('occupation', 'orator')]
        lp = ListPack(deets, sep='# ', padding=' ', indentation=2)
        assert str(lp) == '\n  \x1b[1mname\x1b[0m# Cicero \x1b[1moccupation\x1b[0m# orator '

    def test_calc(self):
        assert ListPack().calc(('name', 'Cicero')) == 14

    def test_append_item(self):
        lp = ListPack([('a', 'b')])
        lp.append_item(('c', 'd'))
        assert str(lp) == '\n\x1b[1ma\x1b[0m: b  \x1b[1mc\x1b[0m: d  '

    def test_prepend_item(self):
        lp = ListPack([('a', 'b')])
        lp.prepend_item(('c', 'd'))
        assert str(lp) == '\n\x1b[1mc\x1b[0m: d  \x1b[1ma\x1b[0m: b  '
