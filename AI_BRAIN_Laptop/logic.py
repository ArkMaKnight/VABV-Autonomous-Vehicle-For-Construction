def test_security(data):
    get_hard_hat = data.get('hard_hat', 0) > 0
    get_vest = data.get('vest', 0) > 0

    if get_hard_hat and get_vest:
        return True, "SE HAN DETECTADO EQUIPOS DE PROTECCIÓN"
    else: 
        return False, "NO SE HAN DETECTADO EQUIPOS DE PROTECCIÓN" 
    