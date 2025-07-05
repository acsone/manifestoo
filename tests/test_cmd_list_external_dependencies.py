from manifestoo.commands.list_external_dependencies import (
    list_external_dependencies_command,
)
from manifestoo.main import app

from .common import (
    CliRunner,
    mock_addons_selection,
    mock_addons_set,
    populate_addons_dir,
)


def tests_basic():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"external_dependencies": {"deb": ["imagemagick"]}},
        }
    )
    assert list_external_dependencies_command(
        mock_addons_selection("a"), addons_set, "deb", transitive=False
    ) == (
        [],
        set(),
    )


def tests_transitive():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"external_dependencies": {"deb": ["imagemagick"]}},
        }
    )
    assert list_external_dependencies_command(
        mock_addons_selection("a"), addons_set, "deb", transitive=True
    ) == (
        ["imagemagick"],
        set(),
    )


def tests_missing():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"], "external_dependencies": {"deb": ["imagemagick"]}},
        }
    )
    assert list_external_dependencies_command(
        mock_addons_selection("a"), addons_set, "deb", True
    ) == (
        ["imagemagick"],
        {"b"},
    )


def test_integration(tmp_path):
    addons = {
        "a": {"depends": ["b"], "external_dependencies": {"deb": ["curl", "wget"]}},
        "b": {"external_dependencies": {"deb": ["imagemagick"]}},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            f"--select-addons-dir={tmp_path}",
            "list-external-dependencies",
            "deb",
            "--transitive",
        ],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == "curl\nimagemagick\nwget\n"
