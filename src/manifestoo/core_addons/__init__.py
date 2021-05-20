"""List of Odoo official addons."""

import sys
from functools import lru_cache
from typing import Dict, Iterable, Set

if sys.version_info >= (3, 9):
    from importlib.resources import open_text
else:
    from importlib_resources import open_text

from ..odoo_series import OdooSeries


@lru_cache()
def _get_core_addons(odoo_series: OdooSeries, ce: str) -> Set[str]:
    with open_text(
        "manifestoo.core_addons", f"addons-{odoo_series.value}-{ce}.txt"
    ) as f:
        return {a.strip() for a in f if not a.startswith("#")}


def get_core_addons(odoo_series: OdooSeries) -> Set[str]:
    return _get_core_addons(odoo_series, "c") | _get_core_addons(odoo_series, "e")


def is_core_addon(addon_name: str, odoo_series: OdooSeries) -> bool:
    return addon_name in get_core_addons(odoo_series)
