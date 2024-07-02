from typing import Dict, List, Optional, Set

import typer

from manifestoo_core.addon import Addon
from manifestoo_core.addons_set import AddonsSet
from manifestoo_core.core_addons import (
    is_core_addon,
    is_core_ce_addon,
    is_core_ee_addon,
)
from manifestoo_core.odoo_series import OdooEdition, OdooSeries

from ..addons_selection import AddonsSelection

NodeKey = str


class Node:
    def __init__(self, addon_name: str, addon: Optional[Addon]):
        self.addon_name = addon_name
        self.addon = addon
        self.children = []  # type: List[Node]

    @staticmethod
    def key(addon_name: str) -> NodeKey:
        return addon_name

    def print(self, odoo_series: OdooSeries, fold_core_addons: bool) -> None:
        seen: Set[Node] = set()

        def _print(indent: List[str], node: Node) -> None:
            # inspired by https://stackoverflow.com/a/59109706
            SPACE = "    "
            BRANCH = "│   "
            TEE = "├── "
            LAST = "└── "
            typer.echo(f"{''.join(indent)}{node.addon_name}", nl=False)
            if node in seen:
                typer.secho(" ⬆", dim=True)
                return
            typer.secho(f" ({node.sversion(odoo_series)})", dim=True)
            seen.add(node)
            if not node.children:
                return
            if fold_core_addons and is_core_addon(node.addon_name, odoo_series):
                return
            pointers = [TEE] * (len(node.children) - 1) + [LAST]
            for pointer, child in zip(
                pointers, sorted(node.children, key=lambda n: n.addon_name)
            ):
                if indent:
                    if indent[-1] == TEE:
                        _print(indent[:-1] + [BRANCH, pointer], child)
                    else:
                        assert indent[-1] == LAST
                        _print(indent[:-1] + [SPACE, pointer], child)
                else:
                    _print([pointer], child)

        _print([], self)

    def sversion(self, odoo_series: OdooSeries) -> str:
        if not self.addon:
            return typer.style("✘ not installed", fg=typer.colors.RED)
        elif is_core_ce_addon(self.addon_name, odoo_series):
            return f"{odoo_series.value}+{OdooEdition.CE.value}"
        elif is_core_ee_addon(self.addon_name, odoo_series):
            return f"{odoo_series.value}+{OdooEdition.EE.value}"
        else:
            return self.addon.manifest.version or "no version"


def tree_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    odoo_series: OdooSeries,
    fold_core_addons: bool,
) -> None:
    nodes: Dict[NodeKey, Node] = {}

    def add(addon_name: str) -> Node:
        key = Node.key(addon_name)
        if key in nodes:
            return nodes[key]
        addon = addons_set.get(addon_name)
        node = Node(addon_name, addon)
        nodes[key] = node
        if not addon:
            # not found
            return node
        for depend in addon.manifest.depends:
            if depend == "base":
                continue
            node.children.append(add(depend))
        return node

    root_nodes: List[Node] = []
    for addon_name in sorted(addons_selection):
        if addon_name == "base":
            continue
        root_nodes.append(add(addon_name))
    for root_node in root_nodes:
        root_node.print(odoo_series, fold_core_addons)
