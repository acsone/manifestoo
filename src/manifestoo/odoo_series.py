from enum import Enum
from typing import Optional, Set

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
    v15_0 = "15.0"
    v16_0 = "16.0"


class OdooEdition(str, Enum):
    CE = "c"
    EE = "e"


def detect_from_addon_version(version: str) -> Optional[OdooSeries]:
    parts = version.split(".")
    if len(parts) < 5:
        return None
    try:
        return OdooSeries["v" + "_".join(parts[:2])]
    except KeyError:
        return None


def detect_from_addons_set(addons_set: AddonsSet) -> Optional[OdooSeries]:
    detected: Set[OdooSeries] = set()
    for addon in addons_set.values():
        addon_version = addon.manifest.version
        if not addon_version:
            continue
        addon_series = detect_from_addon_version(addon_version)
        if not addon_series:
            continue
        detected.add(addon_series)
    if len(detected) == 0:
        echo.notice("No Odoo series detected in addons set")
        return None
    elif len(detected) > 1:
        echo.notice(
            f"Different Odoo series detected in addons set: {', '.join(detected)}"
        )
        return None
    return detected.pop()
