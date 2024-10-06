from bank import value

def test_hello():
    assert value("Hello, Newman") == 0
    assert value("hello its nice day") == 0


def test_h():
    assert value("How doing") == 20
    assert value("How are you") == 20

def test_noth():
    assert value("what's up man") == 100
    assert value("what's happening?") == 100

