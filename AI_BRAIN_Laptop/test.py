import pytest 
from logic import test_security

def test_case_secure(): 
    input_data = {'hard_hat': 1, 'vest': 1, 'person': 1}
    safe, msg = test_security(input_data)

    assert 