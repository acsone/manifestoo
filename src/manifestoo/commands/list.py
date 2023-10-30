from typing import Iterable, Optional

from manifestoo_core.addons_set import AddonsSet

from ..addon_sorter import AddonSorter, AddonSorterAlphabetical
from ..addons_selection import AddonsSelection


def list_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    addon_sorter: Optional[AddonSorter] = None,
) -> Iterable[str]:
    if not addon_sorter:
        addon_sorter = AddonSorterAlphabetical()
    return addon_sorter.sort(addons_selection, addons_set)
