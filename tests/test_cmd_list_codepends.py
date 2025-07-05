import sys

import pytest

from manifestoo.addon_sorter import AddonSorterTopological
from manifestoo.commands.list_codepends import list_codepends_command
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
    addons_selection = mock_addons_selection("b")
    assert list_codepends_command(
        addons_selection, addons_set, transitive=False, include_selected=False
    ) == ["a"]


def test_transitive():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"depends": ["c"]},
            "c": {},
        }
    )
    addons_selection = mock_addons_selection("c")
    assert list_codepends_command(
        addons_selection, addons_set, transitive=False, include_selected=False
    ) == ["b"]
    assert list_codepends_command(
        addons_selection, addons_set, transitive=True, include_selected=False
    ) == ["a", "b"]


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires python3.9 or higher")
def test_transitive_topological():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"depends": ["c"]},
            "c": {},
        }
    )
    addons_selection = mock_addons_selection("c")
    assert list_codepends_command(
        addons_selection,
        addons_set,
        transitive=False,
        include_selected=False,
        addon_sorter=AddonSorterTopological(),
    ) == ["b"]
    assert list_codepends_command(
        addons_selection,
        addons_set,
        transitive=True,
        include_selected=False,
        addon_sorter=AddonSorterTopological(),
    ) == ["b", "a"]


def test_loop():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"depends": ["c"]},
            "c": {"depends": ["a"]},
        }
    )
    addons_selection = mock_addons_selection("a")
    assert list_codepends_command(
        addons_selection, addons_set, transitive=False, include_selected=False
    ) == ["c"]
    assert list_codepends_command(
        addons_selection, addons_set, transitive=True, include_selected=False
    ) == ["b", "c"]
    assert list_codepends_command(
        addons_selection, addons_set, transitive=True, include_selected=True
    ) == ["a", "b", "c"]


def test_include_selected_not_included():
    """Dependencies that are part of the selection are not returned."""
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {},
        }
    )
    addons_selection = mock_addons_selection("a,b")
    assert (
        list_codepends_command(addons_selection, addons_set, include_selected=False)
        == []
    )


def test_include_selected():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {},
        }
    )
    addons_selection = mock_addons_selection("b")
    assert list_codepends_command(
        addons_selection, addons_set, include_selected=False
    ) == ["a"]
    assert list_codepends_command(
        addons_selection, addons_set, include_selected=True
    ) == ["a", "b"]


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires python3.9 or higher")
def test_include_selected_topological():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {},
        }
    )
    addons_selection = mock_addons_selection("b")
    assert list_codepends_command(
        addons_selection,
        addons_set,
        include_selected=False,
        addon_sorter=AddonSorterTopological(),
    ) == ["a"]
    assert list_codepends_command(
        addons_selection,
        addons_set,
        include_selected=True,
        addon_sorter=AddonSorterTopological(),
    ) == ["b", "a"]


def test_integration(tmp_path):
    addons = {
        "a": {"depends": ["b"]},
        "b": {},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [f"--addons-path={tmp_path}", "--select-include", "a", "list-codepends"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == "a\n"
