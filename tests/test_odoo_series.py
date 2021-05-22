from manifestoo.odoo_series import (
    OdooSeries,
    detect_from_addon_version,
    detect_from_addons_set,
)

from .common import mock_addons_set


def test_detect_from_version():
    assert detect_from_addon_version("1.0.0") is None
    assert detect_from_addon_version("1.0.0.0.0.0") is None
    assert detect_from_addon_version("8.0.1") is None
    assert detect_from_addon_version("8.0.1.0") is None
    assert detect_from_addon_version("8.0.1.0.0") == OdooSeries.v8_0
    assert detect_from_addon_version("14.0.1.0.0.1") == OdooSeries.v14_0


def test_detect_none():
    addons_set = mock_addons_set(
        {
            "a": {"version": "1.0.0"},
            "b": {},
        }
    )
    assert detect_from_addons_set(addons_set) is None


def test_detect_one():
    addons_set = mock_addons_set(
        {
            "a": {"version": "1.0.0"},
            "b": {"version": "12.0.1.0.0"},
        }
    )
    assert detect_from_addons_set(addons_set) is OdooSeries.v12_0


def test_detect_ambiguous():
    addons_set = mock_addons_set(
        {
            "a": {"version": "13.0.1.0.0"},
            "b": {"version": "12.0.1.0.0"},
        }
    )
    assert detect_from_addons_set(addons_set) is None
