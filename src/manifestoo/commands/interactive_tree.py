from typing import List, Optional

from textual.app import App, ComposeResult
from textual.widgets import Header, Tree

from manifestoo_core.addon import Addon
from manifestoo_core.addons_set import AddonsSet
from manifestoo_core.core_addons import (
    is_core_addon,
    is_core_ce_addon,
    is_core_ee_addon,
)
from manifestoo_core.odoo_series import OdooEdition, OdooSeries

from ..addons_selection import AddonsSelection


class Context:
    def __init__(
        self,
        addons_set: AddonsSet,
        odoo_series: OdooSeries,
        fold_core_addons: bool,
    ) -> None:
        self.addons_set = addons_set
        self.odoo_series = odoo_series
        self.fold_core_addons = fold_core_addons


class Node:
    def __init__(
        self,
        addon_name: str,
        addon: Optional[Addon],
        context: Context,
    ):
        self.addon_name = addon_name
        self.addon = addon
        self.context = context

    def __str__(self) -> str:
        return f"{self.addon_name} {self._version_str}"

    @property
    def _version_str(self) -> str:
        if not self.addon:
            return "✘ not installed"
        elif is_core_ce_addon(self.addon_name, self.context.odoo_series):
            return f"{self.context.odoo_series.value}+{OdooEdition.CE.value}"
        elif is_core_ee_addon(self.addon_name, self.context.odoo_series):
            return f"{self.context.odoo_series.value}+{OdooEdition.EE.value}"
        else:
            return self.addon.manifest.version or "no version"

    def has_children(self) -> bool:
        return bool(self.children())

    def children(self) -> List["Node"]:
        if not self.addon:
            return []
        if self.context.fold_core_addons and is_core_addon(
            self.addon_name, self.context.odoo_series
        ):
            return []
        children = []
        for depend in self.addon.manifest.depends:
            if depend == "base":
                continue
            children.append(
                Node(
                    depend,
                    self.context.addons_set.get(depend),
                    self.context,
                )
            )
        return children


class ManifestooTree(Tree[Node]):
    def __init__(self, root_nodes: List[Node]) -> None:
        super().__init__(label="...")
        for root_node in root_nodes:
            self.root.add(
                str(root_node),
                data=root_node,
                expand=False,
                allow_expand=root_node.has_children(),
            )

    def on_tree_node_expanded(self, event: Tree.NodeExpanded[Node]) -> None:
        if event.node._children:
            # aldready expanded once
            return
        if event.node.data is None:
            # to please mypy
            return
        for child in event.node.data.children():
            event.node.add(
                str(child),
                data=child,
                expand=False,
                allow_expand=child.has_children(),
            )


class ManifestooTreeApp(App[None]):
    """Manifestoo tree."""

    def __init__(self, root_nodes: List[Node]) -> None:
        super().__init__()
        self.root_nodes = root_nodes

    def compose(self) -> ComposeResult:
        yield Header()
        tree = ManifestooTree(self.root_nodes)
        tree.show_root = False
        yield tree


def interactive_tree_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    odoo_series: OdooSeries,
    fold_core_addons: bool,
) -> None:
    context = Context(addons_set, odoo_series, fold_core_addons)
    root_nodes = [
        Node(
            addon_name,
            addons_set.get(addon_name),
            context,
        )
        for addon_name in addons_selection
    ]
    app = ManifestooTreeApp(root_nodes)
    app.title = "Manifestoo tree"
    app.run()
