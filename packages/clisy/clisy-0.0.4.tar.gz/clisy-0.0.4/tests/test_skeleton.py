from clisy.skeleton import main

__author__ = "Nilesh Kumar"
__copyright__ = "Nilesh Kumar"
__license__ = "MIT"


def test_main_ddg(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["--ddg", "clisy"])
    captured = capsys.readouterr()
    assert "" in captured.out


def test_main_g(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["-g", "clisy"])
    captured = capsys.readouterr()
    assert "" in captured.out


def test_main_w(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["-w", "clisy"])
    captured = capsys.readouterr()
    assert "" in captured.out


def test_main_wc(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["--wc", "clisy"])
    captured = capsys.readouterr()
    assert "" in captured.out


def test_main_a(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["-a", "clisy"])
    captured = capsys.readouterr()
    assert "" in captured.out


def test_main_cci(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["--cci", "clisy"])
    captured = capsys.readouterr()
    assert "" in captured.out


def test_main_imdb(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["--imdb", "clisy"])
    captured = capsys.readouterr()
    assert "" in captured.out


def test_main_swiggy(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["--sw", "clisy"])
    captured = capsys.readouterr()
    assert "" in captured.out
