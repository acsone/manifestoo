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
