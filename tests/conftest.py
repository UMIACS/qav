
import pytest


@pytest.fixture
def give_input(monkeypatch):
    '''Emit one value each time get_input is called.'''
    def give_input_wrapper(question, values):
        def mock_input(self):
            return values.pop(0)

        monkeypatch.setattr(question, '_get_input', mock_input)

    return give_input_wrapper
