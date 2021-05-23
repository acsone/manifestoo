from manifestoo.dependency_iterator import dependency_iterator

from .common import mock_addons_set


def test_basic():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"depends": ["c"]},
        }
    )
    assert sorted(
        addon_name
        for addon_name, _ in dependency_iterator(
            ["a", "c"], addons_set, transitive=False
        )
    ) == ["a", "c"]
    assert sorted(
        addon_name
        for addon_name, _ in dependency_iterator(
            ["a", "c"], addons_set, transitive=True
        )
    ) == ["a", "b", "c"]


def test_loop():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"depends": ["c"]},
            "c": {"depends": ["a"]},
        }
    )
    assert sorted(
        addon_name
        for addon_name, _ in dependency_iterator(
            ["a", "c"], addons_set, transitive=True
        )
    ) == ["a", "b", "c"]
