from typing import Iterable, Optional, Set

from manifestoo_core.addon import Addon
from manifestoo_core.addons_set import AddonsSet
from manifestoo_core.core_addons import is_core_addon
from manifestoo_core.odoo_series import OdooSeries

from ..addons_selection import AddonsSelection
from ..dependency_iterator import dependency_iterator

CORE_DEV_STATUS = "core"
CORE_DEV_STATUS_LEVEL = 100
DEV_STATUS_LEVELS = {
    "alpha": 1,
    "beta": 2,
    "production/stable": 3,
    "production": 3,
    "stable": 3,
    "mature": 4,
}


def _get_dev_status(
    addon: Addon,
    default_dev_status: Optional[str],
    odoo_series: OdooSeries,
    errors: Set[str],
) -> Optional[str]:
    if is_core_addon(addon.name, odoo_series):
        return CORE_DEV_STATUS
    dev_status = addon.manifest.development_status or default_dev_status
    if not dev_status:
        errors.add(f"{addon.name} has missing development_status")
        return None
    if dev_status.lower() not in DEV_STATUS_LEVELS:
        errors.add(f"{addon.name} has invalid development_status {dev_status!r}")
        return None
    return dev_status


def _get_dev_status_level(dev_status: str) -> int:
    if dev_status.lower() == CORE_DEV_STATUS:
        return CORE_DEV_STATUS_LEVEL
    return DEV_STATUS_LEVELS[dev_status.lower()]


def check_dev_status_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    default_dev_status: Optional[str],
    transitive: bool,
    odoo_series: OdooSeries,
) -> Iterable[str]:
    errors: Set[str] = set()
    for addon_name, addon in dependency_iterator(
        addons_selection, addons_set, transitive
    ):
        if not addon:
            errors.add(f"{addon_name} not found")
            continue
        addon_dev_status = _get_dev_status(
            addon, default_dev_status, odoo_series, errors
        )
        if not addon_dev_status:
            continue
        for depend_name in addon.manifest.depends:
            depend = addons_set.get(depend_name)
            if not depend:
                errors.add(f"{depend_name} not found")
                continue
            depend_dev_status = _get_dev_status(
                depend, default_dev_status, odoo_series, errors
            )
            if not depend_dev_status:
                continue
            addon_level = _get_dev_status_level(addon_dev_status)
            depend_level = _get_dev_status_level(depend_dev_status)
            if addon_level > depend_level:
                errors.add(
                    f"{addon_name} ({addon_dev_status}) depends on "
                    f"{depend_name} ({depend_dev_status})"
                )
    return sorted(errors)
