# -*- coding: utf-8 -*-

import pytest

from qav.questions import Question, QuestionSet
from qav.validators import (
    Validator,
    YesNoValidator,
)


class TestQuestionSet(object):

    def test_init(self):
        qs = QuestionSet()
        assert qs.questions == []
        assert qs.ask() == {}

    def test_add_remove(self):
        qs = QuestionSet()
        q1 = Question('foo', 'foo')
        q2 = Question('bar', 'bar')
        qs.add(q1).add(q2)
        assert len(qs.questions) == 2
        qs.remove(q1)
        assert qs.questions == [q2]
        qs.remove(q2)
        assert qs.questions == []

    def test_ask(self, give_input):
        qs = QuestionSet()
        q1 = Question('foo', 'foo')
        q2 = Question('bar', 'bar')
        qs.add(q1).add(q2)
        give_input(q1, ['98'])
        give_input(q2, ['99'])
        assert qs.ask() == {'foo': '98', 'bar': '99'}


class TestQuestion(object):

    def test_init(self):
        # want to ensure that the two positional args are correct
        question = Question('Your age?', 'age')
        assert question.question == 'Your age?'
        assert question.value == 'age'
        assert isinstance(question.validator, Validator)

    def test_equals(self):
        q1 = Question('Your age?', 'age')
        q2 = Question('Your age?', 'age')
        q3 = Question('Your height?', 'height')
        assert q1 == q2
        assert q1 != q3
        assert q2 != q3

    def test_ask(self, give_input):
        q = Question('Your age?', 'age')
        give_input(q, ['99'])
        assert q.ask() == {'age': '99'}

    def test_multiple_validators(self, give_input):
        class FooValidator(Validator):

            def validate(self, value):
                if 'foo' in value:
                    self._choice = value
                    return True
                else:
                    return False

        class BarValidator(Validator):

            def validate(self, value):
                if 'bar' in value:
                    self._choice = value
                    return True
                else:
                    return False

        q = Question(
            'Your favorite variable name?', 'varname',
            validator=[FooValidator(), BarValidator()]
        )
        give_input(q, ['foobar'])

        assert q.ask() == {'varname': 'foobar'}

    def test_multiple_answers(self, give_input):
        question = Question(
            'Your favorite ice cream flavors?', 'flavors',
            multiple=True)
        give_input(question, ['chocolate', 'vanilla', '.'])
        assert question.ask() == {'flavors': ['chocolate', 'vanilla']}

    def test_answer(self, give_input):
        q = Question(
            'Are you a machine?', 'is_machine',
            validator=YesNoValidator())
        # try first with bad input that'll fail validator
        assert not q.validate('NO WAY!')  # not of the proper format
        assert q.answer() is None

        # try again with good input
        assert q.validate('no')
        assert q.answer() == 'no'

    def test_ask_with_subquestion(self, give_input):
        question = Question(
            'favorite food?', 'food')
        subquestion = Question('favorite time to eat this food?', 'time')
        question.add(subquestion)
        give_input(question, ['pesto'])
        give_input(subquestion, ['9 PM'])

        assert question.ask() == {'food': 'pesto', 'time': '9 PM'}

    def test_add_non_question_should_fail(self):
        with pytest.raises(Exception):
            Question().add(5)
        with pytest.raises(Exception):
            Question().remove(5)

    def test_remove_question(self):
        q = Question('favorite food?', 'food')
        subq = Question('Why is %(food)s your favorite food?', 'why')
        q.add(subq)
        assert len(q._questions) == 1
        q.remove(subq)
        assert len(q._questions) == 0
