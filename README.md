# Question Answer Validation
A python library for console based raw input based questions with answers and
extensive and extensible validation for answers.

It provides question sets and questions with a recusive set of questions.

```
from qav.question import Question
from qav.validators import ListValidator
q = Question('How old am I', 'age', ListValidator([20, 35, 40]))
q.ask()
print q.answer()
```
