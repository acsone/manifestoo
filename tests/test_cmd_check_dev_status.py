import pytest
from typer.testing import CliRunner

from manifestoo.__main__ import app
from manifestoo.commands.check_dev_status import (
    CORE_DEV_STATUS,
    check_dev_status_command,
)

from .common import mock_addons_selection, mock_addons_set, populate_addons_dir


def test_missing_dev_status():
    addons_set = mock_addons_set(
        {
            "a": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status=None, recursive=False
    )
    assert errors == ["a has missing development_status"]


def test_missing_dev_status_depends():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"], "development_status": "Stable"},
            "b": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status=None, recursive=False
    )
    assert errors == ["b has missing development_status"]


def test_invalid_dev_status():
    addons_set = mock_addons_set(
        {
            "a": {"development_status": "bad"},
            "b": {"development_status": CORE_DEV_STATUS},
        }
    )
    addons_selection = mock_addons_selection("a,b")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status=None, recursive=False
    )
    assert sorted(errors) == [
        "a has invalid development_status 'bad'",
        "b has invalid development_status 'core'",
    ]


def test_invalid_dev_status_depends():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"], "development_status": "Stable"},
            "b": {"development_status": "bad"},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status=None, recursive=False
    )
    assert errors == ["b has invalid development_status 'bad'"]


def test_missing_selection():
    addons_set = mock_addons_set({})
    addons_selection = mock_addons_selection("a")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status="Beta", recursive=False
    )
    assert errors == ["a not found"]


def test_missing_depend():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status="Beta", recursive=False
    )
    assert errors == ["b not found"]


def test_ok():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status="Beta", recursive=False
    )
    assert errors == []


def test_basic():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"development_status": "Alpha"},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status="Beta", recursive=False
    )
    assert errors == ["a (Beta) depends on b (Alpha)"]


def test_double():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"], "development_status": "Stable"},
            "b": {"depends": ["c"], "development_status": "Beta"},
            "c": {"depends": [], "development_status": "Alpha"},
        }
    )
    addons_selection = mock_addons_selection("a,b")
    errors = check_dev_status_command(
        sorted(addons_selection), addons_set, default_dev_status="Beta", recursive=True
    )
    assert sorted(errors) == [
        "a (Stable) depends on b (Beta)",
        "b (Beta) depends on c (Alpha)",
    ]


def test_recursive():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"]},
            "b": {"depends": ["c"]},
            "c": {"development_status": "Alpha"},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status="Beta", recursive=False
    )
    assert errors == []
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status="Beta", recursive=True
    )
    assert errors == ["b (Beta) depends on c (Alpha)"]


@pytest.mark.xfail()
def test_core_addon():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["base"], "development_status": "Stable"},
            "base": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_dev_status_command(
        addons_selection, addons_set, default_dev_status="Beta", recursive=True
    )
    assert errors == []


def test_integration(tmp_path):
    addons = {
        "a": {"depends": ["b"], "development_status": "Beta"},
        "b": {},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(
        app,
        [
            f"--addons-path={tmp_path}",
            "--select-include",
            "a",
            "check-dev-status",
            "--default-dev-status=Alpha",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert result.stdout == "a (Beta) depends on b (Alpha)\n"