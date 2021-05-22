"""List of Odoo official addons."""

import sys
from functools import lru_cache
from typing import Set

if sys.version_info >= (3, 9):
    from importlib.resources import open_text
else:
    from importlib_resources import open_text

from ..license import LicenseType
from ..odoo_series import OdooSeries


@lru_cache()
def _get_core_addons(odoo_series: OdooSeries, ce: str) -> Set[str]:
    with open_text(
        "manifestoo.core_addons", f"addons-{odoo_series.value}-{ce}.txt"
    ) as f:
        return {a.strip() for a in f if not a.startswith("#")}


@lru_cache()
def get_core_addons(odoo_series: OdooSeries) -> Set[str]:
    return _get_core_addons(odoo_series, "c") | _get_core_addons(odoo_series, "e")


def is_core_ce_addon(addon_name: str, odoo_series: OdooSeries) -> bool:
    return addon_name in _get_core_addons(odoo_series, "c")


def is_core_ee_addon(addon_name: str, odoo_series: OdooSeries) -> bool:
    return addon_name in _get_core_addons(odoo_series, "e")


def is_core_addon(addon_name: str, odoo_series: OdooSeries) -> bool:
    return is_core_ce_addon(addon_name, odoo_series) or is_core_ee_addon(
        addon_name,
        odoo_series,
    )


def get_core_addon_license(addon_name: str, odoo_series: OdooSeries) -> str:
    if is_core_ce_addon(addon_name, odoo_series):
        if odoo_series == OdooSeries.v8_0:
            return "AGPL-3"
        return "LGPL-3"
    elif is_core_ee_addon(addon_name, odoo_series):
        return "OEEL-1"
    raise AssertionError(f"{addon_name} is not a core addon.")  # pragma: no cover
