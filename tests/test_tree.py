import textwrap

from manifestoo.main import app

from .common import CliRunner, populate_addons_dir


def test_integration(tmp_path):
    addons = {
        "a": {"version": "13.0.1.0.0", "depends": ["b", "c"]},
        "b": {"depends": ["base", "mail"]},
        "c": {"depends": ["account", "b"]},
        "account": {"depends": ["base"]},
        "base": {},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--select=a", f"--addons-path={tmp_path}", "tree"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == textwrap.dedent(
        """\
            a (13.0.1.0.0)
            ├── b (no version)
            │   └── mail (✘ not installed)
            └── c (no version)
                ├── account (13.0+c)
                └── b ⬆
        """
    )
