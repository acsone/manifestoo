from .addons_path import AddonsPath
from .addons_selection import AddonsSelection
from .addons_set import AddonsSet


class MainOptions:
    def __init__(self) -> None:
        self.addons_path = AddonsPath()
        self.addons_set = AddonsSet()
        self.addons_selection = AddonsSelection()
        self.separator = "\n"
