from manifestoo.odoo_series import OdooSeries, detect_from_addon_version


def test_detect():
    assert detect_from_addon_version("1.0.0") is None
    assert detect_from_addon_version("1.0.0.0.0.0") is None
    assert detect_from_addon_version("8.0.1") is None
    assert detect_from_addon_version("8.0.1.0") is None
    assert detect_from_addon_version("8.0.1.0.0") == OdooSeries.v8_0
    assert detect_from_addon_version("14.0.1.0.0.1") == OdooSeries.v14_0
