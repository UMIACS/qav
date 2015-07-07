# Question Answer Validation
qav is a Python library for console-based question and answering, with the
ability to validate input.  Answers can be validated based on the information
provided in previous questions.

It provides question sets to group related questions.  QuestionSets can also
have subordinate QuestionSets that are called depth-first.

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
