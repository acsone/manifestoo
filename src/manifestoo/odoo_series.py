from enum import Enum
from typing import Optional

from . import echo
from .addons_set import AddonsSet


class OdooSeries(str, Enum):
    v8_0 = "8.0"
    v9_0 = "9.0"
    v10_0 = "10.0"
    v11_0 = "11.0"
    v12_0 = "12.0"
    v13_0 = "13.0"
    v14_0 = "14.0"


def detect_from_addon_version(version: str) -> Optional[OdooSeries]:
    parts = version.split(".")
    if len(parts) < 5:
        return None
    try:
        return OdooSeries["v" + "_".join(parts[:2])]
    except KeyError:
        return None


def detect_from_addons_set(addons_set: AddonsSet) -> Optional[OdooSeries]:
    detected: Optional[OdooSeries] = None
    for addon in addons_set.values():
        addon_version = addon.manifest.version
        if not addon_version:
            continue
        addon_series = detect_from_addon_version(addon_version)
        if not addon_series:
            continue
        if detected is None:
            detected = addon_series
        if addon_series != detected:
            # different versions detected in the set
            echo.notice(
                f"Different Odoo series detected in addons set: "
                f"{addon_series}, {detected}"
            )
            return None
    return detected
