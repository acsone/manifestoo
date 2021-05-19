"""List of Odoo official addons."""

from typing import Iterable, Set

try:
    from importlib.resources import open_text
except ImportError:
    from importlib_resources import open_text  # python < 3.9

import typer

from .. import echo
from ..odoo_series import OdooSeries


def _addons(suffix: str) -> Set[str]:
    with open_text("manifestoo.core_addons", "addons-%s.txt" % suffix) as f:
        return {a.strip() for a in f if not a.startswith("#")}


_core_addons = {
    OdooSeries.v8_0: _addons("8c"),
    OdooSeries.v9_0: _addons("9c") | _addons("9e"),
    OdooSeries.v10_0: _addons("10c") | _addons("10e"),
    OdooSeries.v11_0: _addons("11c") | _addons("11e"),
    OdooSeries.v12_0: _addons("12c") | _addons("12e"),
    OdooSeries.v13_0: _addons("13c") | _addons("13e"),
    OdooSeries.v14_0: _addons("14c") | _addons("14e"),
}


def is_core_addon(addon_name: str, odoo_series: OdooSeries) -> bool:
    return addon_name in _core_addons[odoo_series]


def get_core_addons(odoo_series: OdooSeries) -> Iterable[str]:
    return _core_addons[odoo_series]
