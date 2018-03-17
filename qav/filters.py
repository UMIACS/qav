# qav (Question Answer Validation)
# Copyright (C) 2015 UMIACS


class Filter(object):

    def __init__(self, string):
        self.string = string


class DynamicFilter(Filter):

    '''
    A Filter that can dynamically prune choices based off of whether
    filterable_func(choice[, table]) returns True or False.
    '''

    def __init__(self, filterable_func):
        self.filterable_func = filterable_func

    def filter(self, value, table=None):
        '''
        Return True if the value should be pruned; False otherwise.

        If a `table` argument was provided, pass it to filterable_func.
        '''
        if table is not None:
            filterable = self.filterable_func(value, table)
        else:
            filterable = self.filterable_func(value)
        return filterable


class SubFilter(Filter):

    '''
    SubFilter keeps those choices containing a given substring.
    '''

    def filter(self, value, table=None):
        if table is not None and self.string in table:
            s = table[self.string]
        else:
            s = self.string
        if value.count(s) > 0:
            return False
        else:
            return True


class PreFilter(Filter):

    '''
    PreFilter keeps those choices starting with a given substring.
    '''

    def filter(self, value, table=None):
        if table is not None and self.string in table:
            s = table[self.string]
        else:
            s = self.string
        if value.startswith(s):
            return False
        else:
            return True


class PostFilter(Filter):

    '''
    PostFilter keeps those choices ending with a given substring.
    '''

    def filter(self, value, table=None):
        if table is not None and self.string in table:
            s = table[self.string]
        else:
            s = self.string
        if value.endswith(s):
            return False
        else:
            return True
