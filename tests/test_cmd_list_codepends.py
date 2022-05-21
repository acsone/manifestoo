from typer.testing import CliRunner

from manifestoo.commands.list_codepends import list_codepends_command
from manifestoo.main import app

from .common import mock_addons_selection, mock_addons_set, populate_addons_dir


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
    ) == {"a"}


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
    ) == {"b"}
    assert list_codepends_command(
        addons_selection, addons_set, transitive=True, include_selected=False
    ) == {"b", "a"}


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
    ) == {"c"}
    assert list_codepends_command(
        addons_selection, addons_set, transitive=True, include_selected=False
    ) == {"b", "c"}
    assert list_codepends_command(
        addons_selection, addons_set, transitive=True, include_selected=True
    ) == {"a", "b", "c"}


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
        == set()
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
    ) == {"a"}
    assert list_codepends_command(
        addons_selection, addons_set, include_selected=True
    ) == {"a", "b"}


def test_integration(tmp_path):
    addons = {
        "a": {"depends": ["b"]},
        "b": {},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(
        app,
        [f"--addons-path={tmp_path}", "--select-include", "a", "list-codepends"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == "a\n"
