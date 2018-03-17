# -*- coding: utf-8 -*-

from qav.filters import (
    DynamicFilter,
    SubFilter,
    PreFilter,
    PostFilter,
)
from qav.validators import ListValidator


class TestFilters(object):

    def test_dynamic_filter(self):
        def filter_things_with_foo(value, choices):
            return 'foo' in value

        def filter_things_with_bar(value, choices):
            return 'bar' in value

        choices = ['foo', 'bar', 'baz']

        assert set(ListValidator(choices).choices) == set(['foo', 'bar', 'baz'])

        prune_foo_validator = ListValidator(
            choices,
            filters=[DynamicFilter(filter_things_with_foo)])
        assert prune_foo_validator.choices == ['bar', 'baz']

        prune_foo_and_bar_validator = ListValidator(
            choices,
            filters=[
                DynamicFilter(filter_things_with_foo),
                DynamicFilter(filter_things_with_bar),
            ])
        assert prune_foo_and_bar_validator.choices == ['baz']


    def test_sub_filter(self):
        # subfilter should keep choices containing a given string
        choices = ['foo', 'bar', 'baz']
        validator = ListValidator(
            choices,
            filters=[SubFilter('a')])
        assert validator.choices == ['bar', 'baz']

    def test_pre_filter(self):
        choices = ['foo', 'bar', 'baz']
        validator = ListValidator(
            choices,
            filters=[PreFilter('f')])
        assert validator.choices == ['foo']

    def test_post_filter(self):
        choices = ['foo', 'bar', 'baz']
        validator = ListValidator(
            choices,
            filters=[PostFilter('r')])
        assert validator.choices == ['bar']
