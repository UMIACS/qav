class Filter(object):

    def __init__(self, string):
        self.string = string


class SubFilter(Filter):

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

    def filter(self, value, table=None):
        if table is not None and self.string in table:
            s = table[self.string]
        else:
            s = self.string
        if value.endswith(s):
            return False
        else:
            return True
