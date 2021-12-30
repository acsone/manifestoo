from typing import Iterable, Set

from ..addons_selection import AddonsSelection
from ..addons_set import AddonsSet


def list_codepends_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    transitive: bool = True,
    include_selected: bool = True,
) -> Iterable[str]:
    result: Set[str] = set(addons_selection) if include_selected else set()
    codeps = direct_codependencies(addons_selection, addons_set, result)
    result |= codeps
    while transitive and codeps:
        codeps = direct_codependencies(codeps, addons_set, result)
        result |= codeps
    return result if include_selected else result - addons_selection


def direct_codependencies(
    root_addons: Set[str], addons_set: AddonsSet, accumulator: Set[str]
) -> Set[str]:
    return {
        a
        for a in addons_set
        if set(addons_set[a].manifest.depends) & root_addons and a not in accumulator
    }
