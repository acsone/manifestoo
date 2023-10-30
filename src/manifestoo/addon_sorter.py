import sys
from typing import Dict, Iterable, Set

import typer

from manifestoo_core.addons_set import AddonsSet

from . import echo
from .exceptions import CycleErrorExit


class AddonSorter:
    @staticmethod
    def from_name(name: str) -> "AddonSorter":
        if name == "alphabetical":
            return AddonSorterAlphabetical()
        elif name == "topological":
            if sys.version_info < (3, 9):
                echo.error(
                    "The 'topological' sorter requires Python 3.9 or later",
                    err=False,
                )
                raise typer.Exit(1)
            return AddonSorterTopological()
        else:
            echo.error(f"Unknown sorter {name}", err=False)
            raise typer.Exit(1)

    def sort(
        self, addons_selection: Iterable[str], addon_set: AddonsSet
    ) -> Iterable[str]:
        raise NotImplementedError()


class AddonSorterAlphabetical(AddonSorter):
    def sort(
        self, addons_selection: Iterable[str], addon_set: AddonsSet
    ) -> Iterable[str]:
        return sorted(addons_selection)


class AddonSorterTopological(AddonSorter):
    def sort(
        self, addons_selection: Iterable[str], addon_set: AddonsSet
    ) -> Iterable[str]:
        result_dict: Dict[str, Set[str]] = {}
        for addon_name in addons_selection:
            try:
                addon = addon_set[addon_name]
                result_dict[addon_name] = set(
                    depend
                    for depend in addon.manifest.depends
                    if depend in addons_selection
                )
            except KeyError:
                echo.debug(f"Addon {addon_name} not found in addon set")
        from graphlib import CycleError, TopologicalSorter

        topological_sorted_res = TopologicalSorter(result_dict)
        try:
            res = list(topological_sorted_res.static_order())
        except CycleError as e:
            echo.error("Cycle detected in dependencies", err=False)
            raise CycleErrorExit(1) from e
        return res
