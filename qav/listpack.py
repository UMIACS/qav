import random
import string


class ListPack(object):
    BOLD='\033[1m'
    OFF='\033[0m'

    def __init__(self, lp):
        self.sep = ": "
        self.buf = "  "
        self.width = 79
        self._lp = lp

    def calc(self, t):
        s1, s2 = t
        return len(str(s1)) + len(self.sep) + len(str(s2)) + len(self.buf)

    def bold(self, t):
        s1, s2 = t
        return '%s%s%s%s%s%s' % (self.BOLD, str(s1), self.OFF, self.sep, str(s2), self.buf)

    def append_item(self, item):
        self._lp.append(item)

    def prepend_item(self, item):
        self._lp.insert(0, item)

    def __str__(self):
        _str = ''
        line = ''
        line_length = 0
        for i in self._lp:
            if line_length + self.calc(i) > self.width:
                if _str != '':
                    _str = _str + '\n' + line
                else:
                    _str = line
                line = self.bold(i)
                line_length = self.calc(i)
            else:
                line += self.bold(i)
                line_length += self.calc(i)
        _str = _str + '\n' + line
        return _str


def id_generator(size=6, chars=None):
    if chars is None:
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    letter = random.choice(string.ascii_lowercase)
    return letter + ''.join(random.choice(chars) for x in range(size))


def lp_generator(size=20):
    lp = []
    for i in range(size):
        lp.append((id_generator(size=random.randint(4,15)),
                  id_generator(size=random.randint(6,60))))
    return lp


if __name__ == "__main__":
    lp = ListPack([('hostname', 'novelty.umiacs.umd.edu'),
                   ('architecture', 'x86_64'),
                   ('ipaddress', '128.8.120.234'),
                   ('netmask', '255.255.255.0'),
                   ('gateway', '128.8.120.1'),
                   ('macaddress', 'aa:bb:cc:dd:ee:ff'),
                   ('cr',None)])
    print lp
    for x in range(10):
        print ListPack(lp_generator())
        print "--------------------------------------------------"
