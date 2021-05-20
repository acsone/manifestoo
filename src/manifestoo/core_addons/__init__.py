"""List of Odoo official addons."""

from functools import lru_cache
from typing import Dict, Iterable, Set

try:
    from importlib.resources import open_text
except ImportError:
    from importlib_resources import open_text  # python < 3.9

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
