import contextlib

import pytest

from manifestoo import echo


@contextlib.contextmanager
def _verbosity(n):
    saved_verbosity = echo.verbosity
    echo.verbosity = n
    try:
        yield
    finally:
        echo.verbosity = saved_verbosity


@pytest.mark.parametrize()
def _test_verbosity(func, threshold, capsys):
    with _verbosity(threshold - 1):
        # no output below threshold
        func("msg")
        assert "msg" not in capsys.readouterr().err
    with _verbosity(threshold):
        # verbosity on or above verbosity
        func("msg")
        assert capsys.readouterr().err == "msg\n"


def test_debug(capsys):
    _test_verbosity(echo.debug, 2, capsys)


def test_info(capsys):
    _test_verbosity(echo.info, 1, capsys)


def test_notice(capsys):
    _test_verbosity(echo.notice, 0, capsys)


def test_warning(capsys):
    _test_verbosity(echo.warning, -1, capsys)


def test_echo_error(capsys):
    echo.error("msg")
    assert capsys.readouterr().err == "msg\n"


def test_echo_error_low_verbosity(capsys):
    # no threshold for error messages
    with _verbosity(-10):
        echo.error("msg")
        assert capsys.readouterr().err == "msg\n"


def test_echo_to_stdout(capsys):
    echo.error("msg", err=False)
    assert capsys.readouterr().out == "msg\n"
