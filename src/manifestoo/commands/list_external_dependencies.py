from typing import Iterable, Set, Tuple

from ..addons_selection import AddonsSelection
from ..addons_set import AddonsSet
from ..dependency_iterator import dependency_iterator


def list_external_dependencies_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    kind: str,
    recursive: bool = False,
) -> Tuple[Iterable[str], Iterable[str]]:
    result: Set[str] = set()
    missing: Set[str] = set()
    for addon_name, addon in dependency_iterator(
        addons_selection, addons_set, recursive
    ):
        if not addon:
            missing.add(addon_name)
        else:
            result.update(addon.manifest.external_dependencies.get(kind, []))
    return sorted(result), missing
