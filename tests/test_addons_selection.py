from manifestoo.addons_selection import AddonsSelection

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
