import sys
from pathlib import Path

from manifestoo.addons_path import AddonsPath


def test_from_addons_dirs():
    addons_path = AddonsPath()
    addons_path.extend_from_addons_dirs([Path("a"), Path("b")])
    assert str(addons_path) == "a,b"


def test_from_addons_path():
    addons_path = AddonsPath()
    addons_path.extend_from_addons_path("a,b")
    assert str(addons_path) == "a,b"


def test_from_odoo_cfg(tmp_path):
    odoo_cfg = tmp_path / "odoo.cfg"
    odoo_cfg.write_text("[options]\naddons_path=a,b\n")
    addons_path = AddonsPath()
    addons_path.extend_from_odoo_cfg(odoo_cfg)
    assert str(addons_path) == "a,b"


def test_from_odoo_cfg__without_addons_path(tmp_path):
    odoo_cfg = tmp_path / "odoo.cfg"
    odoo_cfg.write_text("[options]\n")
    addons_path = AddonsPath()
    addons_path.extend_from_odoo_cfg(odoo_cfg)
    assert str(addons_path) == ""


def test_from_import_odoo__python_not_found():
    addons_path = AddonsPath()
    addons_path.extend_from_import_odoo("this-is-not-a-snake")
    assert str(addons_path) == ""


def test_from_import_odoo__odoo_not_found():
    addons_path = AddonsPath()
    addons_path.extend_from_import_odoo(sys.executable)
    assert str(addons_path) == ""
