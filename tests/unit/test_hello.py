from hello.main import hello


def test_hello():
    """
    Test the hello function simply returns "Hello, world!".
    """
    assert hello() == "Hello, world!"
