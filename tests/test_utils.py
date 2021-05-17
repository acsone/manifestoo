import pytest

from manifestoo.utils import comma_split


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
