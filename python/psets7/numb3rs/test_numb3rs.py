from numb3rs import validate

def test_validate_true():
    assert validate("127.0.0.1") == True
    assert validate("255.255.255.255") == True
    assert validate("1.2.3.4") == True
    assert validate("101.010.001.099") == True


def test_validate_false():
    assert validate("cat") == False
    assert validate("1.2.3.1000") == False
    assert validate("423.342.424.12") == False
    assert validate("23.32.44.932") == False
