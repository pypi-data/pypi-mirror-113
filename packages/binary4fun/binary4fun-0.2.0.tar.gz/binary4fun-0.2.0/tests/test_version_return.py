import sh


def test_should_return_version():
    assert sh.python(["setup.py", "--version"])
