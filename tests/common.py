from pathlib import Path
from typing import Any, Dict

from manifestoo.addon import Addon
from manifestoo.addons_selection import AddonsSelection
from manifestoo.addons_set import AddonsSet
from manifestoo.manifest import Manifest


def populate_addons_dir(addons_dir: Path, addons: Dict[str, Dict[str, Any]]):
    if not addons_dir.is_dir():
        addons_dir.mkdir()
    for addon_name, manifest in addons.items():
        addon_path = addons_dir / addon_name
        addon_path.mkdir()
        (addon_path / "__init__.py").touch()
        manifest_path = addon_path / "__manifest__.py"
        manifest_path.write_text(repr(manifest))


def mock_manifest(
    manifest_dict: Dict[str, Any], addon_name: str = "fake-addon"
) -> Manifest:
    manifest_path = Path("/tmp/fake-addons-dir") / addon_name / "__manifest__.py"
    return Manifest(manifest_path, manifest_dict)


def mock_addons_set(addons: Dict[str, Dict[str, Any]]) -> AddonsSet:
    addons_set = AddonsSet()
    for addon_name, manifest_dict in addons.items():
        manifest = mock_manifest(manifest_dict, addon_name)
        addons_set[addon_name] = Addon(manifest)
    return addons_set


def mock_addons_selection(addon_names: str) -> AddonsSelection:
    addons_selection = AddonsSelection()
    addons_selection.add_addon_names(addon_names)
    return addons_selection
