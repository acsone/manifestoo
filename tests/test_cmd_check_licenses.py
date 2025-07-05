from manifestoo.commands.check_licenses import check_licenses_command
from manifestoo.main import app
from manifestoo_core.odoo_series import OdooSeries

from .common import (
    CliRunner,
    mock_addons_selection,
    mock_addons_set,
    populate_addons_dir,
)


def test_missing_license():
    addons_set = mock_addons_set(
        {
            "a": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_licenses_command(
        addons_selection,
        addons_set,
        transitive=False,
        odoo_series=OdooSeries.v12_0,
    )
    assert errors == []


def test_mit_depends_mit():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"], "license": "MIT"},
            "b": {"license": "MIT"},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_licenses_command(
        addons_selection,
        addons_set,
        transitive=False,
        odoo_series=OdooSeries.v12_0,
    )
    assert errors == []


def test_unknown_license_cant_depend_on_open_source():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"], "license": "My License"},
            "b": {"license": "GPL-3"},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_licenses_command(
        addons_selection,
        addons_set,
        transitive=False,
        odoo_series=OdooSeries.v12_0,
    )
    assert errors == ["a (My License) depends on b (GPL-3)"]


def test_unknown_license_can_depend_on_proprietary():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["b"], "license": "My License"},
            "b": {"license": "Other Proprietary"},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_licenses_command(
        addons_selection,
        addons_set,
        transitive=False,
        odoo_series=OdooSeries.v12_0,
    )
    assert errors == []


def test_v8_agpl():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["account"], "license": "LGPL-3"},
            "account": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_licenses_command(
        addons_selection,
        addons_set,
        transitive=False,
        odoo_series=OdooSeries.v8_0,
    )
    assert errors == ["a (LGPL-3) depends on account (AGPL-3)"]


def test_v12_ce_lgpl():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["account"], "license": "LGPL-3"},
            "account": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_licenses_command(
        addons_selection,
        addons_set,
        transitive=False,
        odoo_series=OdooSeries.v12_0,
    )
    assert errors == []


def test_v12_ee_proprietary():
    addons_set = mock_addons_set(
        {
            "a": {"depends": ["account_accountant"], "license": "LGPL-3"},
            "account_accountant": {},
        }
    )
    addons_selection = mock_addons_selection("a")
    errors = check_licenses_command(
        addons_selection,
        addons_set,
        transitive=False,
        odoo_series=OdooSeries.v12_0,
    )
    assert errors == ["a (LGPL-3) depends on account_accountant (OEEL-1)"]


def test_integration(tmp_path):
    addons = {
        "a": {"depends": ["b"], "license": "GPL-3"},
        "b": {"depends": ["c", "d"], "license": "AGPL-3"},
        "d": {"license": "LGPL-3"},
    }
    populate_addons_dir(tmp_path, addons)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            f"--addons-path={tmp_path}",
            "--select-include=a",
            "--odoo-series=13.0",
            "check-licenses",
            "--transitive",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert result.stdout == "a (GPL-3) depends on b (AGPL-3)\nc not found\n"
