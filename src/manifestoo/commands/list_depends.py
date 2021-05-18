from typing import Iterable, Set, Tuple

from manifestoo.addon import Addon
from manifestoo.addons_selection import AddonsSelection
from manifestoo.addons_set import AddonsSet


def _add_depends(
    addon: Addon,
    addons_set: AddonsSet,
    recursive: bool,
    result: Set[str],
    missing: Set[str],
) -> None:
    depends = set(addon.manifest.get("depends", []))
    new_depends = depends - result
    result.update(new_depends)
    if recursive:
        for depend in new_depends:
            try:
                depend_addon = addons_set[depend]
            except KeyError:
                missing.add(depend)
                continue
            _add_depends(depend_addon, addons_set, recursive, result, missing)


def list_depends_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    recursive: bool = False,
    include_selected: bool = False,
) -> Tuple[Iterable[str], Iterable[str]]:
    result: Set[str] = set()
    missing: Set[str] = set()
    for addon_name in addons_selection:
        try:
            addon = addons_set[addon_name]
        except KeyError:
            missing.add(addon_name)
            continue
        _add_depends(addon, addons_set, recursive, result, missing)
    if include_selected:
        result.update(addons_selection)
    return sorted(result), missing
