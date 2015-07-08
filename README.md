# Question Answer Validation

qav is a Python library for console-based question and answering, with the
ability to validate input.

It provides question sets to group related questions.  Questions can also
have subordinate Questions underneath them.  Answers to those questions can be
validated based on a simple, static piece of information provided by you.
Answers mail also be validated dynamically based on the information provided in
previous questions.

## Example Usage
```
>>> from qav.questions import Question
>>> from qav.validators import ListValidator
>>> q = Question('How old am I? ', 'age', ListValidator(['20', '35', '40']))
>>> q.ask()
Please select from the following choices:
 [0] - 20
 [1] - 35
 [2] - 40
How old am I? : 0
>>> q.answer()
# returns => {'age': '20'}
```
