# qav (Question Answer Validation)
# Copyright (C) 2015 UMIACS

from typing import List, Tuple


class ListPack(object):
    BOLD = '\033[1m'
    OFF = '\033[0m'

    def __init__(self, lp=None, sep: str = ": ", padding: str = "  ",
                 indentation: int = 0, width: int = 79) -> None:
        self.sep = sep
        self.padding = padding
        self.indentation = indentation
        self.width = width
        if lp:
            self._lp = lp
        else:
            self._lp = []

        self.new_line = '' + (' ' * self.indentation)

    def calc(self, t: List) -> int:
        s1, s2 = t
        return len(str(s1)) + len(self.sep) + len(str(s2)) + len(self.padding)

    def bold(self, t: List) -> str:
        s1, s2 = t
        return '%s%s%s%s%s%s' % (self.BOLD, str(s1), self.OFF, self.sep,
                                 str(s2), self.padding)

    def append_item(self, item: Tuple['str', 'str']) -> None:
        self._lp.append(item)

    def prepend_item(self, item: Tuple['str', 'str']) -> None:
        self._lp.insert(0, item)

    def __str__(self) -> str:
        _str = ''
        line = self.new_line
        line_length = len(line)
        for i in self._lp:
            if line_length + self.calc(i) > self.width:
                if _str != '':
                    _str = _str + '\n' + line
                else:
                    _str = line
                line = self.new_line + self.bold(i)
                line_length = len(self.new_line) + self.calc(i)
            else:
                line += self.bold(i)
                line_length += self.calc(i)
        _str = _str + '\n' + line
        return _str
