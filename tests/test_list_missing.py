from manifestoo.main import app

from .common import CliRunner, populate_addons_dir


def test_list_missing(tmp_path):
    addons = {
        "a": {"depends": ["c"]},
        "b": {"depends": ["d"]},
        "e": {"depends": ["a", "b"]},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [f"--select-addons-dir={tmp_path}", "list-missing"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == "c\nd\n"
