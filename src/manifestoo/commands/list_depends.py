from typing import Iterable, Optional, Set, Tuple

from manifestoo_core.addons_set import AddonsSet

from ..addon_sorter import AddonSorter, AddonSorterAlphabetical
from ..addons_selection import AddonsSelection
from ..dependency_iterator import dependency_iterator


def list_depends_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    transitive: bool = False,
    include_selected: bool = False,
    addon_sorter: Optional[AddonSorter] = None,
) -> Tuple[Iterable[str], Iterable[str]]:
    if not addon_sorter:
        addon_sorter = AddonSorterAlphabetical()
    result: Set[str] = set()
    missing: Set[str] = set()
    for addon_name, addon in dependency_iterator(
        addons_selection, addons_set, transitive
    ):
        if include_selected:
            result.add(addon_name)
        if not addon:
            missing.add(addon_name)
        else:
            result.update(set(addon.manifest.depends) - set(addons_selection))
    return addon_sorter.sort(result, addons_set), missing
