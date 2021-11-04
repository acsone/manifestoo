from enum import Enum
from typing import Dict, Optional


class LicenseType(Enum):
    PROPRIETARY = 1
    PERMISSIVE = 2  # MIT, Apache
    WEAKLY_PROTECTIVE = 3  # LGPL
    STRONGLY_PROTECTIVE = 4  # GPL
    NETWORK_PROTECTIVE = 5  # AGPL


def can_depend_on(work_license: LicenseType, dependency_license: LicenseType) -> bool:
    if work_license == LicenseType.PROPRIETARY:
        return dependency_license in (
            LicenseType.PROPRIETARY,
            LicenseType.PERMISSIVE,
            LicenseType.WEAKLY_PROTECTIVE,
        )
    elif work_license == LicenseType.PERMISSIVE:
        return dependency_license in (LicenseType.PERMISSIVE,)
    elif work_license == LicenseType.WEAKLY_PROTECTIVE:
        return dependency_license in (
            LicenseType.WEAKLY_PROTECTIVE,
            LicenseType.PERMISSIVE,
        )
    elif work_license == LicenseType.STRONGLY_PROTECTIVE:
        return dependency_license in (
            LicenseType.STRONGLY_PROTECTIVE,
            LicenseType.WEAKLY_PROTECTIVE,
            LicenseType.PERMISSIVE,
        )
    elif work_license == LicenseType.NETWORK_PROTECTIVE:
        return dependency_license in (
            LicenseType.NETWORK_PROTECTIVE,
            LicenseType.STRONGLY_PROTECTIVE,
            LicenseType.WEAKLY_PROTECTIVE,
            LicenseType.PERMISSIVE,
        )
    raise AssertionError(
        f"Unhandled license type {work_license!r}."
    )  # pragma: no cover


_licenses: Dict[str, LicenseType] = {
    "other proprietary": LicenseType.PROPRIETARY,
    "oeel-1": LicenseType.PROPRIETARY,
    "opl-1": LicenseType.PROPRIETARY,
    "agpl-3": LicenseType.NETWORK_PROTECTIVE,
    "gpl-3": LicenseType.STRONGLY_PROTECTIVE,
    "gpl-3 or any later version": LicenseType.STRONGLY_PROTECTIVE,
    "lgpl-3": LicenseType.WEAKLY_PROTECTIVE,
    "lgpl-3 or any later version": LicenseType.WEAKLY_PROTECTIVE,
    "mit": LicenseType.PERMISSIVE,
}


def get_license_type(license: str) -> Optional[LicenseType]:
    return _licenses.get(license.lower())
