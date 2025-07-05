from typing import Iterable, Optional, Set, Tuple

from manifestoo_core.addon import Addon
from manifestoo_core.addons_set import AddonsSet
from manifestoo_core.core_addons import get_core_addon_license, is_core_addon
from manifestoo_core.odoo_series import OdooSeries

from .. import echo
from ..addons_selection import AddonsSelection
from ..dependency_iterator import dependency_iterator
from ..license import LicenseType, can_depend_on, get_license_type


def _get_license_type_or_proprietary(
    addon: Addon, odoo_series: OdooSeries
) -> Tuple[Optional[str], LicenseType]:
    addon_license: Optional[str] = None
    if is_core_addon(addon.name, odoo_series):
        addon_license = get_core_addon_license(addon.name, odoo_series)
    else:
        addon_license = addon.manifest.license
    if not addon_license:
        echo.warning(f"No license declared for {addon.name}, assuming Proprietary.")
        return addon_license, LicenseType.PROPRIETARY
    addon_license_type = get_license_type(addon_license)
    if not addon_license_type:
        echo.warning(
            f"Unknown license {addon_license} for {addon.name}, assuming Proprietary."
        )
        return addon_license, LicenseType.PROPRIETARY
    return addon_license, addon_license_type


def check_licenses_command(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
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
        addon_license, addon_license_type = _get_license_type_or_proprietary(
            addon, odoo_series
        )
        for depend_name in addon.manifest.depends:
            depend = addons_set.get(depend_name)
            if not depend:
                errors.add(f"{depend_name} not found")
                continue
            depend_license, depend_license_type = _get_license_type_or_proprietary(
                depend, odoo_series
            )
            if not can_depend_on(addon_license_type, depend_license_type):
                errors.add(
                    f"{addon_name} ({addon_license}) depends on "
                    f"{depend_name} ({depend_license})"
                )
    return sorted(errors)
