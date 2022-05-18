from typing import Optional

from manifestoo_core.addons_set import AddonsSet
from manifestoo_core.odoo_series import OdooSeries

from .addons_path import AddonsPath
from .addons_selection import AddonsSelection


class MainOptions:
    def __init__(self) -> None:
        self.addons_path = AddonsPath()
        self.addons_set = AddonsSet()
        self.addons_selection = AddonsSelection()
        self.separator: Optional[str] = None  # deprecated
        self.odoo_series: Optional[OdooSeries] = None
