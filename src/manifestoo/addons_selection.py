from pathlib import Path
from typing import List, Set

from manifestoo_core.addons_set import AddonsSet

from .utils import comma_split


class AddonsSelection(Set[str]):
    def __str__(self) -> str:
        return ",".join(sorted(self))

    def add_addons_dirs(self, addons_dirs: List[Path]) -> None:
        addons_set = AddonsSet()
        addons_set.add_from_addons_dirs(addons_dirs)
        self.update(addons_set.keys())

    def add_addon_names(self, addon_names: str) -> None:
        for addon_name in comma_split(addon_names):
            self.add(addon_name)

    def remove_addon_names(self, addon_names: str) -> None:
        for addon_name in comma_split(addon_names):
            try:
                self.remove(addon_name)
            except KeyError:
                pass

    def filter_categories(self, addons_categories: str, addons_set: AddonsSet) -> None:
        categories_list = [category for category in comma_split(addons_categories)]
        addons_list = list(self)
        for addon_name in addons_list:
            addon = addons_set.get(addon_name)
            if addon and addon.manifest.category not in categories_list:
                self.remove(addon_name)
