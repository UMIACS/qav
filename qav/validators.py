# qav (Question Answer Validation)
# Copyright (C) 2015 UMIACS

from __future__ import absolute_import
from __future__ import print_function

import re
import socket
import datetime
import time
from copy import copy
from collections import OrderedDict

from netaddr import IPAddress
from netaddr.core import AddrFormatError

from .utils import nonesorter


class Validator(object):

    '''
    Validator asserts if an answer given is acceptable.  It does this through
    the return value of validate().

    Validators can also transform an acceptable value by setting `_choice`.
    Think of the example of a date being passed in as a string, being
    validated, and then transformed into a datetime object...

    If validation failed, an error message can be set.
    '''

    def __init__(self, blank=False, negate=False):
        self.blank = blank
        self.negate = negate  # TODO this doesn't get used internally..........
        self._choice = None
        self._hints = {}
        self.answers = {}
        self.error_message = None

    def validate(self, value):
        '''The most basic validation'''
        if not self.blank and value == '':
            self.error_message = 'Can not be empty.  Please provide a value.'
            return False
        self._choice = value
        return True

    def choice(self):
        return self._choice

    def print_choices(self):
        return True

    def hints(self):
        return self._hints

    def error(self):
        if self.error_message is not None:
            return 'ERROR: %s' % self.error_message
        else:
            return ''

    @staticmethod
    def stringify(value):
        return str(value)


class YesNoValidator(Validator):

    def validate(self, value):
        if value.lower() in ['yes', 'no']:
            self._choice = value.lower()
            return True
        else:
            self.error_message = 'Please choose yes or no.'
            return False


class CompactListValidator(Validator):

    '''
    Accepts a list of choices like ListValidator but doesn't print
    validator choices.
    '''

    def __init__(self, choices):
        self._choices = choices
        super(CompactListValidator, self).__init__()

    def validate(self, value):
        if value.lower() in self._choices:
            # TODO should this really call lower()?
            self._choice = value.lower()
            return True
        else:
            self.error_message = 'Please choose %s.' % '/'.join(self._choices)
            return False


class DateValidator(Validator):

    '''Accepts dates in the format YYYYMMDD'''

    date_regex = re.compile(r'\d{8}')

    def validate(self, value):
        if self.blank and value == '':
            return True
        if DateValidator.date_regex.match(value):
            # TODO this should account for the GMT offset
            try:
                date = time.strptime(value, "%Y%m%d")
            except ValueError:
                return False
            self._choice = datetime.datetime(*date[:6])
            return True
        else:
            return False


class DomainNameValidator(Validator):

    def validate(self, value):
        """Attempts a forward lookup via the socket library and if
           successful will try to do a reverse lookup to verify DNS
           is returning both lookups.
           """
        if '.' not in value:
            self.error_message = '%s is not a fully qualified domain name.' % \
                                 value
            return False
        try:
            ipaddress = socket.gethostbyname(value)
        except socket.gaierror:
            self.error_message = '%s does not resolve.' % value
            return False
        try:
            socket.gethostbyaddr(ipaddress)
        except socket.herror:
            self.error_message = \
                '%s reverse address (%s) does not resolve.' % \
                (value, ipaddress)
            return False
        self._choice = value
        return True


class MacAddressValidator(Validator):

    macaddr_regex = re.compile(r'^([0-9a-f]{2}[:]){5}([0-9a-f]{2})$')

    def validate(self, value):
        if MacAddressValidator.macaddr_regex.match(value.lower()):
            self._choice = value
            return True
        else:
            self.error_message = '%s is not a valid MAC address.' % value
            return False


class IPAddressValidator(Validator):

    def validate(self, value):
        """Return a boolean if the value is valid"""
        try:
            self._choice = IPAddress(value)
            return True
        except (ValueError, AddrFormatError):
            self.error_message = '%s is not a valid IP address.' % value
            return False


class IPNetmaskValidator(Validator):

    def validate(self, value):
        """Return a boolean if the value is a valid netmask."""
        try:
            self._choice = IPAddress(value)
        except (ValueError, AddrFormatError):
            self.error_message = '%s is not a valid IP address.' % value
            return False
        if self._choice.is_netmask():
            return True
        else:
            self.error_message = '%s is not a valid IP netmask.' % value
            return False


class URIValidator(Validator):

    # taken from Django URL validator
    uri_regex = re.compile(
        r'^\w+:(?://)?'  # uri scheme
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # NOQA
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def validate(self, value):
        '''Return a boolean indicating if the value is a valid URI'''
        if self.blank and value == '':
            return True
        if URIValidator.uri_regex.match(value):
            self._choice = value
            return True
        else:
            self.error_message = '%s is not a valid URI' % value
            return False


class EmailValidator(Validator):

    email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')

    def validate(self, value):
        if self.blank and value == '':
            return True
        if EmailValidator.email_regex.match(value) and len(value) > 3:
            self._choice = value
            return True
        else:
            self.error_message = '%s is not a valid email address.' % value
            return False


class ListValidator(Validator):

    def __init__(self, choices, filters=None):
        self._choices = choices
        if filters is None:
            self.filters = []
        else:
            self.filters = filters
        super(ListValidator, self).__init__()

    @property
    def choices(self):
        _choices = copy(self._choices)
        for c in self._choices:
            for f in self.filters:
                if f.filter(c, self.answers):
                    _choices.remove(c)
                    break
        _choices.sort(key=nonesorter)
        return _choices

    def print_choices(self):
        if len(self.choices) > 0:
            print("Please select from the following choices:")
            for x, y in enumerate(self.choices):
                print(" [%d] - %s" % (x, str(y)))
            return True
        else:
            return False

    def validate(self, value):
        """Return a boolean if the choice is a number in the enumeration"""
        if value in self.choices:
            self._choice = value
            return True
        try:
            self._choice = self.choices[int(value)]
            return True
        except (ValueError, IndexError):
            self.error_message = '%s is not a valid choice.' % value
            return False


class TupleValidator(Validator):

    def __init__(self, choices, filters=None):
        assert isinstance(choices, list)
        self._choices = choices
        if filters is None:
            self.filters = []
        else:
            self.filters = filters
        super(TupleValidator, self).__init__()

    @property
    def choices(self):
        _choices = copy(self._choices)
        for c in self._choices:
            for f in self.filters:
                if f.filter(c, self.answers):
                    _choices.remove(c)
                    break
        _choices.sort()
        return _choices

    def print_choices(self):
        if len(self.choices) > 0:
            print("Please select from the following choices:")
            for x, y in enumerate(self.choices):
                a, b = y
                print(" [%d] - %s (%s)" % (x, a, b))
            return True
        else:
            return False

    def validate(self, value):
        """Return a boolean if the choice a number in the enumeration"""
        for x, y in self.choices:
            if x == value:
                self._choice = value
                return True
        try:
            self._choice = self.choices[int(value)][0]
            return True
        except (ValueError, IndexError):
            self.error_message = '%s is not a valid choice.' % value
            return False


class HashValidator(Validator):

    def __init__(self, choices, filters=None, verbose=True):
        self._choices = OrderedDict()
        self.verbose = verbose
        for x in choices:
            self._choices[x] = choices[x]
        if filters is None:
            self.filters = []
        else:
            self.filters = filters
        super(HashValidator, self).__init__()

    @property
    def choices(self):
        _choices = copy(self._choices)
        for c in self._choices:
            for f in self.filters:
                if f.filter(_choices[c], self.answers):
                    del _choices[c]
                    break
        return _choices

    def print_choices(self):
        if len(self.choices) > 0:
            print("Please select from the following choices:")
            for x, y in enumerate(self.choices):
                if self.verbose:
                    print(" [%d] - %s (%s)" % (x, y, self.choices[y]))
                else:
                    print(" [%d] - %s" % (x, y))
            return True
        else:
            return False

    def validate(self, value):
        """Return a boolean if the choice is a number in the enumeration"""
        if value in list(self.choices.keys()):
            self._choice = value
            return True
        try:
            self._choice = list(self.choices.keys())[int(value)]
            return True
        except (ValueError, IndexError):
            self.error_message = '%s is not a valid choice.' % value
            return False


class IntegerValidator(Validator):

    def validate(self, value):
        """
        Return True if the choice is an integer; False otherwise.

        If the value was cast successfully to an int, set the choice that will
        make its way into the answers dict to the cast int value, not the
        string representation.
        """
        try:
            int_value = int(value)
            self._choice = int_value
            return True
        except ValueError:
            self.error_message = '%s is not a valid integer.' % value
            return False
