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

    def remove_addon_authors(
        self, excluded_authors: Set[str], addons_set: AddonsSet
    ) -> None:
        excluded_addons = set()
        for addon_name in self:
            addon = addons_set.get(addon_name)
            if addon is None:
                continue
            for author in comma_split(addon.manifest.author):
                if author in excluded_authors:
                    excluded_addons.add(addon_name)
                    break
            else:
                if not addon.manifest.author and "" in excluded_authors:
                    excluded_addons.add(addon_name)
        self.difference_update(excluded_addons)

    def remove_addon_names(self, addon_names: str) -> None:
        for addon_name in comma_split(addon_names):
            try:
                self.remove(addon_name)
            except KeyError:
                pass
