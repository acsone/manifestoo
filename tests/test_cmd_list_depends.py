import sys

import pytest

from manifestoo.addon_sorter import AddonSorterTopological
from manifestoo.commands.list_depends import list_depends_command
from manifestoo.exceptions import CycleErrorExit
from manifestoo.main import app

from .common import (
    CliRunner,
    mock_addons_selection,
    mock_addons_set,
    populate_addons_dir,
)


def test_basic():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    assert list_depends_command(addons_selection, addons_set, transitive=False) == (
        ["b"],
        set(),
    )


def test_transitive():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"depends": ["c"]},
            "c": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    assert list_depends_command(addons_selection, addons_set, transitive=False) == (
        ["b"],
        set(),
    )
    assert list_depends_command(addons_selection, addons_set, transitive=True) == (
        [
            "b",
            "c",
        ],
        set(),
    )


def test_loop():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"depends": ["c"]},
            "c": {"depends": ["a"]},
        }
    )
    addons_selection = mock_addons_selection("a")
    assert list_depends_command(addons_selection, addons_set, transitive=True) == (
        [
            "b",
            "c",
        ],
        set(),
    )
    assert list_depends_command(
        addons_selection, addons_set, include_selected=True, transitive=True
    ) == (
        [
            "a",
            "b",
            "c",
        ],
        set(),
    )


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires python3.9 or higher")
def test_loop_topological():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"depends": ["c"]},
            "c": {"depends": ["a"]},
        }
    )
    addons_selection = mock_addons_selection("a")
    with pytest.raises(CycleErrorExit):
        list_depends_command(
            addons_selection,
            addons_set,
            include_selected=True,
            transitive=True,
            addon_sorter=AddonSorterTopological(),
        )


def test_missing():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
        }
    )
    assert list_depends_command(
        mock_addons_selection("a"), addons_set, transitive=False
    ) == (
        [
            "b",
        ],
        set(),
    )
    assert list_depends_command(
        mock_addons_selection("a"), addons_set, transitive=True
    ) == (
        [
            "b",
        ],
        {"b"},
    )
    assert list_depends_command(
        mock_addons_selection("a,c"), addons_set, transitive=True
    ) == (
        [
            "b",
        ],
        {"b", "c"},
    )
    assert list_depends_command(
        mock_addons_selection("a,c"), addons_set, include_selected=True, transitive=True
    ) == (
        ["a", "b", "c"],
        {"b", "c"},
    )


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires python3.9 or higher")
def test_missing_topological():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
        }
    )
    assert list_depends_command(
        mock_addons_selection("a,c"),
        addons_set,
        include_selected=True,
        transitive=True,
        addon_sorter=AddonSorterTopological(),
    ) == (
        ["b", "a"],
        {"b", "c"},
    )


def test_include_selected_not_included():
    """Dependencies that are part of the selection are not returned."""
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {},
        }
    )
    addons_selection = mock_addons_selection("a,b")
    assert list_depends_command(
        addons_selection, addons_set, include_selected=False
    ) == (
        [],
        set(),
    )


def test_include_selected():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    assert list_depends_command(
        addons_selection, addons_set, include_selected=True
    ) == (
        [
            "a",
            "b",
        ],
        set(),
    )


def test_integration(tmp_path):
    addons = {
        "a": {"depends": ["b"]},
        "b": {},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [f"--addons-path={tmp_path}", "--select-include", "a", "list-depends"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == "b\n"
