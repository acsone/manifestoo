from typing import Iterable, Optional, Set

from manifestoo_core.addons_set import AddonsSet

from ..addon_sorter import AddonSorter, AddonSorterAlphabetical
from ..addons_selection import AddonsSelection


def list_codepends_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    transitive: bool = True,
    include_selected: bool = True,
    addon_sorter: Optional[AddonSorter] = None,
) -> Iterable[str]:
    if not addon_sorter:
        addon_sorter = AddonSorterAlphabetical()
    result: Set[str] = set(addons_selection) if include_selected else set()
    codeps = direct_codependencies(addons_selection, addons_set, result)
    result |= codeps
    while transitive and codeps:
        codeps = direct_codependencies(codeps, addons_set, result)
        result |= codeps
    res = result if include_selected else result - addons_selection
    return addon_sorter.sort(res, addons_set)


def direct_codependencies(
    root_addons: Set[str], addons_set: AddonsSet, accumulator: Set[str]
) -> Set[str]:
    return {
        a
        for a in addons_set
        if set(addons_set[a].manifest.depends) & root_addons and a not in accumulator
    }
