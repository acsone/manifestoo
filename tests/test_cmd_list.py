import json

from typer.testing import CliRunner

from manifestoo.commands.list import list_command
from manifestoo.main import app

from .common import mock_addons_selection, populate_addons_dir


def test_basic():
    addons_selection = mock_addons_selection("b,a")
    assert list_command(addons_selection) == ["a", "b"]


def test_integration(tmp_path):
    addons = {
        "a": {},
        "b": {},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(
        app,
        [f"--select-addons-dir={tmp_path}", "list"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == "a\nb\n"


def test_integration_json(tmp_path):
    addons = {
        "a": {"name": "A"},
        "b": {},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(
        app,
        [f"--select-addons-dir={tmp_path}", "list", "--format=json"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    json_output = json.loads(result.stdout)
    assert "a" in json_output
    assert "b" in json_output
    assert "manifest" in json_output["a"]
    assert "manifest_path" in json_output["a"]
    assert "path" in json_output["a"]
    assert json_output["a"]["manifest"] == addons["a"]
