import textwrap
from pathlib import Path

from manifestoo.main import app

from .common import CliRunner, populate_addons_dir


def _init_test_addons(tmp_path: Path):
    addons = {
        "a": {"version": "13.0.1.0.0", "depends": ["b", "c"]},
        "b": {"depends": ["base", "mail"]},
        "c": {"depends": ["account", "b"]},
        "account": {"depends": ["base"]},
        "base": {},
    }
    populate_addons_dir(tmp_path, addons)


def test_integration(tmp_path: Path):
    _init_test_addons(tmp_path)
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


def test_integration_inverse(tmp_path: Path):
    _init_test_addons(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--select=a", f"--addons-path={tmp_path}", "tree", "--inverse"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0, result.stderr
    assert result.stdout == textwrap.dedent(
        """\
            account (13.0+c)
            └── c (no version)
                └── a (13.0.1.0.0)
            mail (✘ not installed)
            └── b (no version)
                ├── a (13.0.1.0.0)
                └── c (no version)
                    └── a ⬆
        """
    )


def test_integration_unfold_seen_addons(tmp_path: Path):
    _init_test_addons(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--select=a", f"--addons-path={tmp_path}", "tree", "--unfold-seen-addons"],
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
                └── b (no version)
                    └── mail (✘ not installed)
        """
    )
