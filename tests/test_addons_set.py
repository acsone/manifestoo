from manifestoo.addons_set import AddonsSet

from .common import populate_addons_dir


def test_from_addons_dir(tmp_path):
    addons = {
        "a": {},
        "b": {},
        "c": {"installable": False},
    }
    populate_addons_dir(tmp_path, addons)
    addons_set = AddonsSet()
    addons_set.add_from_addons_dir(tmp_path)
    assert str(addons_set) == "a,b"


def test_from_addons_dirs(tmp_path):
    addons1 = {
        "a": {},
        "b": {},
    }
    addons_dir_1 = tmp_path / "addons_dir_1"
    populate_addons_dir(addons_dir_1, addons1)
    addons2 = {
        "c": {},
    }
    addons_dir_2 = tmp_path / "addons_dir_2"
    populate_addons_dir(addons_dir_2, addons2)
    addons_set = AddonsSet()
    addons_set.add_from_addons_dirs([addons_dir_1, addons_dir_2])
    assert str(addons_set) == "a,b,c"


def test_from_missing_dir(tmp_path):
    addons_set = AddonsSet()
    addons_set.add_from_addons_dirs([tmp_path / "not-a-dir"])
    assert str(addons_set) == ""
