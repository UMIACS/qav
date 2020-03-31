# qav (Question Answer Validation)
# Copyright (C) 2015 UMIACS


BOLD = '\033[1m'
OFF = '\033[0m'


def bold(s: str) -> str:
    return '%s%s%s' % (BOLD, str(s), OFF)


def nonesorter(elem) -> str:
    """Allow NoneType to be sortable.  Used as a key function."""
    if not elem:
        return ""
    return elem
