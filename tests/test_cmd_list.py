from textwrap import dedent

from typer.testing import CliRunner

from manifestoo.commands.list import list_command
from manifestoo.main import app

from .common import mock_addons_selection, mock_addons_set, populate_addons_dir


def test_basic():
    addons_selection = mock_addons_selection("b,a")
    addons_set = mock_addons_set(
        {
            "a": {},
            "b": {},
        }
    )
    assert list_command(addons_selection, addons_set) == ["a", "b"]


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


def test_found(tmp_path):
    addons = {"a": {}, "b": {}, "c": {"installable": False}}
    populate_addons_dir(tmp_path, addons)
    conf = tmp_path / "odoo.conf"
    conf.write_text(
        dedent(
            f"""\
            [options]
            addons_path = {tmp_path}
            """
        )
    )
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(
        app,
        ["--select-found", "list"],
        catch_exceptions=False,
        env={"ODOO_RC": str(conf)},
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == "a\nb\n"
