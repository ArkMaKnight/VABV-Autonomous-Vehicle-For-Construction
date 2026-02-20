import pytest 
from logic import test_security

def test_case_secure(): 
    input_data = {'hard_hat': 1, 'vest': 1, 'person': 1}
    safe, msg = test_security(input_data)

    assert safe == True
    assert msg == "SE HAN DETECTADO EQUIPOS DE PROTECCIÓN"

def test_case_insecure():
    input_data = {'hard_hat': 0, 'vest': 1, 'person': 1}
    safe, msg = test_security(input_data)

    assert safe == False
    assert msg == "NO SE HAN DETECTADO EQUIPOS DE PROTECCIÓN"

def test_empty_case():
    input_data = {}
    safe, msg = test_security(input_data)

    assert safe == True

