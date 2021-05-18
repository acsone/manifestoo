import pytest
import typer

from manifestoo.utils import comma_split, not_implemented, notice_or_abort, print_list


@pytest.mark.parametrize(
    "s, expected",
    [
        (None, []),
        ("", []),
        ("  ", []),
        (" a", ["a"]),
        ("a, b", ["a", "b"]),
        ("a,,b, c ", ["a", "b", "c"]),
    ],
)
def test_comma_split(s, expected):
    assert comma_split(s) == expected


def test_print_list(capsys):
    print_list(["b", "a"], ",")
    assert capsys.readouterr().out == "b,a\n"


def test_print_empty_list(capsys):
    print_list([], ",")
    assert capsys.readouterr().out == ""


def test_not_implemented(capsys):
    with pytest.raises(typer.Abort):
        not_implemented("msg")
    assert capsys.readouterr().err == "msg is not implemented.\n"


def test_notice_or_abort(capsys):
    notice_or_abort("msg", False)
    assert capsys.readouterr().err == "msg\n"
    with pytest.raises(typer.Abort):
        notice_or_abort("msg", True)
    assert capsys.readouterr().err == "msg\n"
