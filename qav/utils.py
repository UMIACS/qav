# qav (Question Answer Validation)
# Copyright (C) 2015 UMIACS


BOLD = '\033[1m'
OFF = '\033[0m'


def bold(s):
    return '%s%s%s' % (BOLD, str(s), OFF)
