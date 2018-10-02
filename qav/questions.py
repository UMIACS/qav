# qav (Question Answer Validation)
# Copyright (C) 2015 UMIACS

from __future__ import absolute_import
from __future__ import print_function

# hack to support python2 and python3
try:
    input = raw_input
except NameError:
    pass

import logging

from qav.validators import Validator, CompactListValidator
from qav.listpack import ListPack
from qav.utils import bold

logger = logging.getLogger(__name__)


class QuestionSet(object):

    def __init__(self):
        self.answers = {}
        self.questions = []

    def add(self, question):
        self.questions.append(question)
        return self

    def remove(self, question):
        self.questions.remove(question)
        return self

    def ask(self):
        for question in self.questions:
            self.answers = dict(self.answers, **question.ask(self.answers))
        return self.answers

    def ask_and_confirm(self, additional_readonly_items=None,
                        prepend_listpacking_items=True):
        confirm_question = Question('Are these answers correct? ' +
                                    '[yes/abort/retry]', value='confirm',
                                    validator=CompactListValidator(
                                        choices=['yes', 'abort', 'retry']))

        while True:
            answers = self.ask()
            lp = ListPack(
                [(q.printable_name, answers[q.value]) for q in self.questions])

            # add in items that were not asked as questions but should be
            # displayed alongside that information
            if additional_readonly_items:
                if prepend_listpacking_items:
                    for item in additional_readonly_items:
                        lp.prepend_item(item)
                else:
                    for item in additional_readonly_items:
                        lp.append_item(item)

            print(lp)
            confirm_answer = confirm_question.ask()
            if confirm_answer['confirm'] == 'yes':
                return answers
            if confirm_answer['confirm'] != 'retry':
                return None


class Question(object):

    def __init__(self, question, value, validator=None, multiple=False,
                 printable_name=None):
        """ Basic Question class.

            Supports simple question and answer or question and multiple
            answers (note: list/hash validators have caveats).  Also
            support for one or more Validator classes to ensure the answer
            given meets the question criteria.
        """
        self.question = question
        self.value = value
        self.multiple = multiple
        if printable_name:
            self.printable_name = printable_name
        else:
            self.printable_name = value
        if validator is None:
            self.validator = Validator()
        else:
            self.validator = validator
        self._questions = []

    def __eq__(self, other):
        if self.question == other.question and self.value == other.value:
            return True
        else:
            return False

    def __repr__(self):
        return self.value

    def _get_input(self, text):
        return input(text)

    def _ask(self, answers):
        """ Really ask the question.

            We may need to populate multiple validators with answers here.
            Then ask the question and insert the default value if
            appropriate.  Finally call the validate function to check all
            validators for this question and returning the answer.
        """
        if isinstance(self.validator, list):
            for v in self.validator:
                v.answers = answers
        else:
            self.validator.answers = answers
        while(True):
            q = self.question % answers

            if not self.choices():
                logger.warning('No choices were supplied for "%s"' % q)
                return None
            if self.value in answers:
                default = Validator.stringify(answers[self.value])
                answer = self._get_input("%s [%s]: " % (q, default))
                if answer == '':
                    answer = answers[self.value]
            else:
                answer = self._get_input("%s: " % q)
            # if we are in multiple mode and the answer is just the empty
            # string (enter/return pressed) then we will just answer None
            # to indicate we are done
            if answer == '.' and self.multiple:
                return None
            if self.validate(answer):
                return self.answer()
            else:
                if isinstance(self.validator, list):
                    for v in self.validator:
                        if v.error() != '':
                            print(v.error())
                else:
                    print(self.validator.error())

    def ask(self, answers=None):
        """ Ask the question, then ask any sub-questions.

            This returns a dict with the {value: answer} pairs for the current
            question plus all descendant questions.
        """
        if answers is None:
            answers = {}
        _answers = {}
        if self.multiple:
            print((bold('Multiple answers are supported for this question.  ' +
                        'Please enter a "."  character to finish.')))
            _answers[self.value] = []
            answer = self._ask(answers)
            while answer is not None:
                _answers[self.value].append(answer)
                answer = self._ask(answers)
        else:
            _answers[self.value] = self._ask(answers)
        if isinstance(self.validator, list):
            for v in self.validator:
                _answers = dict(_answers, **v.hints())
        else:
            _answers = dict(_answers, **self.validator.hints())
        for q in self._questions:
            answers = dict(answers, **_answers)
            _answers = dict(_answers, **q.ask(answers))
        return _answers

    def validate(self, answer):
        """ Validate the answer with our Validator(s)

            This will support one or more validator classes being applied to
            this question.  If there are multiple, all validators must return
            True for the answer to be valid.
        """
        if answer is None:
            return False
        else:
            if isinstance(self.validator, list):
                for v in self.validator:
                    if not v.validate(answer):
                        return False
                return True
            else:
                return self.validator.validate(answer)

    def answer(self):
        """ Return the answer for the question from the validator.

            This will ultimately only be called on the first validator if
            multiple validators have been added.
        """
        if isinstance(self.validator, list):
            return self.validator[0].choice()
        return self.validator.choice()

    def choices(self):
        """ Print the choices for this question.

            This may be a empty string and in the case of a list of validators
            we will only show the first validator's choices.
        """
        if isinstance(self.validator, list):
            return self.validator[0].print_choices()
        return self.validator.print_choices()

    def add(self, question):
        if isinstance(question, Question):
            self._questions.append(question)
        else:
            # TODO this should raise a less generic exception
            raise Exception

    def remove(self, question):
        if isinstance(question, Question):
            self._questions.remove(question)
        else:
            raise Exception
