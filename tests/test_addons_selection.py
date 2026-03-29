from manifestoo.addons_selection import AddonsSelection
from manifestoo_core.addons_set import AddonsSet

from .common import populate_addons_dir


def test_add_addons_dirs(tmp_path):
    addons = {
        "a": {},
        "b": {},
        "c": {"installable": False},
    }
    populate_addons_dir(tmp_path, addons)
    addons_selection = AddonsSelection()
    addons_selection.add_addons_dirs([tmp_path])
    assert str(addons_selection) == "a,b"  # c is not installable


def test_add_addon_names():
    addons_selection = AddonsSelection()
    addons_selection.add_addon_names("a,b")
    addons_selection.add_addon_names("a,c")
    assert str(addons_selection) == "a,b,c"


def test_add_remove_addon_names():
    addons_selection = AddonsSelection()
    addons_selection.add_addon_names("a,b,c,d")
    addons_selection.remove_addon_names("a,c,e")
    assert str(addons_selection) == "b,d"


def test_select_exclude_authors(tmp_path):
    addons = {
        "addon1": {"author": "Odoo S.A."},
        "addon2": {"author": "Odoo Community Association,Other Contributors"},
        "addon3": {"author": "Addon Creators Inc.,Odoo S.A."},
        "addon4": {"author": "Author 1"},
        "addon5": {"author": "Author 2,Author 3"},
        "addon6": {},
    }
    populate_addons_dir(tmp_path, addons)
    addons_set = AddonsSet()
    addons_set.add_from_addons_dirs([tmp_path])
    addons_selection = AddonsSelection()
    addons_selection.update(addons_set.keys())
    addons_selection.remove_addon_authors(
        ["Odoo S.A.", "Odoo Community Association", ""], addons_set
    )
    assert str(addons_selection) == "addon4,addon5"
