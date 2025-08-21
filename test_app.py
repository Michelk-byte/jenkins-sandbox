from app import hello

def test_default():
    assert hello() == "hello, world!"

def test_custom():
    assert hello("jenkins") == "hello, jenkins!"
