# -*- coding: utf-8 -*-

import datetime
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import pytest
from netaddr import IPAddress

from qav.filters import PreFilter
from qav.validators import (
    Validator,
    CompactListValidator,
    DateValidator,
    DomainNameValidator,
    EmailValidator,
    HashValidator,
    IntegerValidator,
    IPAddressValidator,
    IPNetmaskValidator,
    ListValidator,
    MacAddressValidator,
    TupleValidator,
    URIValidator,
    YesNoValidator,
)


class TestValidator(object):

    def test_validate(self):
        v = Validator()
        assert v.validate('') is False
        assert v.error_message is not None

    def test_blank(self):
        v = Validator(blank=True)
        assert v.validate('') is True
        assert v.choice() == ''

    def test_error(self):
        v = Validator()
        v.validate('')
        assert v.error() == 'ERROR: Can not be empty.  Please provide a value.'

    def test_stringify(self):
        assert Validator.stringify(5) == '5'
        assert Validator.stringify('5') == '5'


class TestYesNoValidator(object):

    @pytest.mark.parametrize('value', ('yes', 'YES', 'no', 'NO'))
    def test_validate_success(self, value):
        v = YesNoValidator()
        assert v.validate(value) == True
        assert v.choice() == value.lower()

    def test_validate_failure(self):
        v = YesNoValidator()
        assert v.validate('something else') == False
        assert v.choice() == None
        assert v.error() == 'ERROR: Please choose yes or no.'


class TestCompactListValidator(object):

    @pytest.mark.parametrize('value', ('foo', 'bar', 'baz'))
    def test_validate_success(self, value):
        v = CompactListValidator(choices=['foo', 'bar', 'baz']) 
        assert v.validate(value) == True
        assert v.choice() == value

    def test_validate_failure(self):
        v = CompactListValidator(choices=['foo', 'bar', 'baz'])
        assert v.validate('junk') == False
        assert v.error() == 'ERROR: Please choose foo/bar/baz.'


class TestDateValidator(object):

    @pytest.mark.parametrize('value,expected_choice', [
        ('20180518', datetime.datetime(2018, 5, 18)),
        ('20120521', datetime.datetime(2012, 5, 21)),
    ])
    def test_validate_success(self, value, expected_choice):
        v = DateValidator()
        assert v.validate(value) == True
        assert v.choice() == expected_choice

    @pytest.mark.parametrize('value', ('20170517 00:00:00', '5/18/1992', 'foo'))
    def test_validate_failure(self, value):
        assert DateValidator().validate(value) == False


class TestDomainNameValidator(object):

    def test_is_fqdn(self):
        v = DomainNameValidator()
        assert v.validate('localhost') == False
        assert v.error() == 'ERROR: localhost is not a fully qualified domain name.'

    def test_does_resolve(self):
        v = DomainNameValidator()
        assert v.validate('google.com') == True
        assert v.choice() == 'google.com'

    def test_does_not_resolve(self):
        v = DomainNameValidator()
        assert v.validate('lsdkajflsdjsldsfjk.com') == False
        assert v.error() == 'ERROR: lsdkajflsdjsldsfjk.com does not resolve.'


class TestMacAddressValidator(object):

    @pytest.mark.parametrize('value', (
        'AA:01:54:21:BB:0F',
        'aa:01:54:21:bb:0f'
    ))
    def test_validate_success(self, value):
        v = MacAddressValidator()
        assert v.validate(value) == True
        assert v.choice() == value

    @pytest.mark.parametrize('value', (
        'AA:01:54:21:BB:0F:55',  # too long
        'AA:01:54:21:BB',        # too short
        'AA 01 54 21 BB 0F',     # bad formats
        'AA015421BB0F',
        'foobar',
    ))
    def test_validate_failure(self, value):
        v = MacAddressValidator()
        assert v.validate(value) == False
        assert v.error() == 'ERROR: %s is not a valid MAC address.' % value


class TestIPAddressValidator(object):

    @pytest.mark.parametrize('value', (
        '192.168.78.10',
        '10.88.88.1',
        '8.8.8.8',
    ))
    def test_validate_success(self, value):
        v = IPAddressValidator()
        assert v.validate(value) == True
        assert v.choice() == IPAddress(value)

    @pytest.mark.parametrize('value', (
        '10.500.10.10',
        '10.20.20.100/24',
        'foobar',
    ))
    def test_validate_failure(self, value):
        v = IPAddressValidator()
        assert v.validate(value) == False
        assert v.error() == 'ERROR: %s is not a valid IP address.' % value


class TestIPNetmaskValidator(object):

    @pytest.mark.parametrize('value', (
        '255.255.255.0',
        '255.255.254.0',
        '0.0.0.0',
    ))
    def test_validate_success(self, value):
        v = IPNetmaskValidator()
        assert v.validate(value) == True
        assert v.choice() == IPAddress(value)

    @pytest.mark.parametrize('value', (
        '62.125.24.5',
        '10.20.20.100/24',
        'foobar',
        '',
    ))
    def test_validate_failure(self, value):
        v = IPNetmaskValidator()
        assert v.validate(value) == False
        assert v.error_message is not None


class TestURIValidator(object):

    @pytest.mark.parametrize('value', (
        'http://google.com',
        'https://google.com',
        'http://localhost',
        'HTTP://GOOGLE.COM',
        'smb://foo.com',
    ))
    def test_validate_success(self, value):
        v = URIValidator()
        assert v.validate(value) == True
        assert v.choice() == value

    @pytest.mark.parametrize('value', (
        'http://example',
        'google.com',
        'http://_*.com',
        'foobar',
        '5'
    ))
    def test_validate_failure(self, value):
        v = URIValidator()
        assert v.validate(value) == False
        assert v.error() == 'ERROR: %s is not a valid URI' % value


class TestEmailValidator(object):

    def test_validate_success(self):
        v = EmailValidator()
        assert v.validate('user@example.com') == True
        assert v.choice() == 'user@example.com'

    @pytest.mark.parametrize('value', (
        'user',
        'user@',
        '@user',
        'user@foo',
    ))
    def test_validate_failure(self, value):
        v = EmailValidator()
        assert v.validate(value) == False
        assert v.error() == 'ERROR: %s is not a valid email address.' % value


class TestListValidator(object):

    def test_filters(self):
        choices = ['one dog', 'two dogs']
        v = ListValidator(choices, filters=[PreFilter('one')])
        assert v.choices == ['one dog']

    def test_choices_get_sorted(self):
        v = ListValidator(['c', 'b', 'f', 'a'])
        assert v.choices == ['a', 'b', 'c', 'f']

    def test_print_choices(self, capsys):
        v = ListValidator(['a', 'b', 'c'])
        assert v.print_choices() == True
        out, err = capsys.readouterr()
        assert out == '''Please select from the following choices:
 [0] - a
 [1] - b
 [2] - c
'''

    def test_no_choices(self):
        v = ListValidator([])
        assert v.print_choices() == False
        assert v.validate('0') == False

    @pytest.mark.parametrize('value,idx', [
        ('a', '0'),
        ('b', '1'),
        ('c', '2'),
    ])
    def test_validate_success(self, value, idx):
        v = ListValidator(['a', 'b', 'c'])
        
        # try passing in the value itself
        assert v.validate(value) == True
        assert v.choice() == value

        # passing in the index number of out choice should work, too
        assert v.validate(idx) == True
        assert v.choice() == value

    def test_validate_failure(self):
        v = ListValidator(['a', 'b', 'c'])
        assert v.validate('d') == False
        assert v.error() == 'ERROR: d is not a valid choice.'
        assert v.validate('5') == False
        assert v.error() == 'ERROR: 5 is not a valid choice.'


class TestTupleValidator(object):

    def test_validate_success(self):
        v = TupleValidator([
            ('ABRT', 'Abort'),
            ('CONT', 'Continue')])
        assert v.choices == [('ABRT', 'Abort'),
            ('CONT', 'Continue')]

    def test_list_of_tuples_passed_as_choice(self):
        with pytest.raises(AssertionError):
            v = TupleValidator(('a', 'b'))
        with pytest.raises(AssertionError):
            v = TupleValidator((
                ('a', 'A'),
                ('b', 'B')))

    def test_print_choices(self, capsys):
        v = TupleValidator([('a', 'A'), ('b', 'B'), ('c', 'C')])
        assert v.print_choices() == True
        out, err = capsys.readouterr()
        assert out == '''Please select from the following choices:
 [0] - a (A)
 [1] - b (B)
 [2] - c (C)
'''

    def test_no_choices(self, capsys): 
        v = TupleValidator([])
        assert v.print_choices() == False
        assert v.validate('0') == False

    @pytest.mark.parametrize('value,idx', [
        ('a', '0'),
        ('b', '1'),
        ('c', '2'),
    ])
    def test_validate_success(self, value, idx):
        v = TupleValidator([('a', 'A'), ('b', 'B'), ('c', 'C')])

        # try passing in the value itself
        assert v.validate(value) == True
        assert v.choice() == value

        # passing in the index number of out choice should work, too
        assert v.validate(idx) == True
        assert v.choice() == value

    def test_validate_failure(self):
        v = TupleValidator([('a', 'A'), ('b', 'B'), ('c', 'C')])
        assert v.validate('d') == False
        assert v.error() == 'ERROR: d is not a valid choice.'
        assert v.validate('5') == False
        assert v.error() == 'ERROR: 5 is not a valid choice.'


class TestHashValidator(object):

    def test_choices(self):
        choices = {'ten': '10', 'twenty': '20'}
        v = HashValidator(choices, filters=[PreFilter('1')])
        assert v.choices == OrderedDict([('ten', '10')])

    def print_choices(self, capsys):
        v = HashValidator({'ten': '10', 'twenty': '20'})
        assert v.print_choices() == True
        out, err = capsys.readouterr()
        assert out == '''Please select from the following choices:
 [0] - ten (10)
 [1] - twenty (20)
'''

    @pytest.mark.parametrize('key,value', [
        ('ten', '10'),
        ('twenty', '20'),
    ])
    def test_validate_success(self, key, value):
        v = HashValidator({'ten': '10', 'twenty': '20'})

        # try passing in the value itself
        assert v.validate(key) == True
        assert v.choice() == key 

    def test_validate_failure(self):
        v = HashValidator({'ten': '10', 'twenty': '20'})
        assert v.validate('d') == False
        assert v.error() == 'ERROR: d is not a valid choice.'
        assert v.validate('5') == False
        assert v.error() == 'ERROR: 5 is not a valid choice.'


class TestIntegerValidator(object):

    @pytest.mark.parametrize('value', ('2', '4', '8'))
    def test_validate_success(self, value):
        v = IntegerValidator()
        assert v.validate(value) == True
        assert v.choice() == int(value)

    @pytest.mark.parametrize('value', ('a2', '4a', 'foo', '7.2'))
    def test_validate_failure(self, value):
        assert IntegerValidator().validate(value) == False
