from manifestoo.addons_path import from_addons_path, from_cli_options, from_odoo_cfg


def test_from_addons_path():
    assert str(from_addons_path("a,b")) == "a, b"


def test_from_odoo_cfg(tmp_path):
    odoo_cfg = tmp_path / "odoo.cfg"
    odoo_cfg.write_text("[options]\naddons_path=a,b\n")
    assert str(from_odoo_cfg(odoo_cfg)) == "a, b"


def test_from_odoo_cfg_without_addons_path(tmp_path):
    odoo_cfg = tmp_path / "odoo.cfg"
    odoo_cfg.write_text("[options]\n")
    assert str(from_odoo_cfg(odoo_cfg)) == ""


def test_from_cli_options(tmp_path):
    odoo_cfg = tmp_path / "odoo.cfg"
    odoo_cfg.write_text("[options]\naddons_path=c,d\n")
    assert str(from_cli_options("a,b", False, "python", odoo_cfg)) == "a, b, c, d"
