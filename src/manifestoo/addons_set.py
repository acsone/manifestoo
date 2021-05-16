from typing import Dict, Iterable
from pathlib import Path

from .addon import Addon, AddonNotFound


class AddonsSet(Dict[str, Addon]):
    @classmethod
    def from_addons_dir(cls, addons_dir: Path) -> "AddonsSet":
        addons_set = AddonsSet()
        for addon_dir in addons_dir.iterdir():
            if not addon_dir.is_dir():
                continue
            try:
                addon = Addon.from_addon_dir(addon_dir)
            except AddonNotFound:
                continue
            else:
                addons_set[addon.name] = addon
        return addons_set

    @classmethod
    def from_addons_dirs(cls, addons_dirs: Iterable[Path]) -> "AddonsSet":
        addons_set = AddonsSet()
        for addons_dir in addons_dirs:
            addons_set.update(cls.from_addons_dir(addons_dir))
        return addons_set
