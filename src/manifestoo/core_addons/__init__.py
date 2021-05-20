"""List of Odoo official addons."""

from typing import Dict, Iterable, Set

try:
    from importlib.resources import open_text
except ImportError:
    from importlib_resources import open_text  # python < 3.9

from ..odoo_series import OdooSeries


def _addons(suffix: str) -> Set[str]:
    with open_text("manifestoo.core_addons", "addons-%s.txt" % suffix) as f:
        return {a.strip() for a in f if not a.startswith("#")}


_core_addons_ce: Dict[OdooSeries, Set[str]] = {
    OdooSeries.v8_0: _addons("8c"),
    OdooSeries.v9_0: _addons("9c"),
    OdooSeries.v10_0: _addons("10c"),
    OdooSeries.v11_0: _addons("11c"),
    OdooSeries.v12_0: _addons("12c"),
    OdooSeries.v13_0: _addons("13c"),
    OdooSeries.v14_0: _addons("14c"),
}

_core_addons_ee: Dict[OdooSeries, Set[str]] = {
    OdooSeries.v8_0: set(),
    OdooSeries.v9_0: _addons("9e"),
    OdooSeries.v10_0: _addons("10e"),
    OdooSeries.v11_0: _addons("11e"),
    OdooSeries.v12_0: _addons("12e"),
    OdooSeries.v13_0: _addons("13e"),
    OdooSeries.v14_0: _addons("14e"),
}

_core_addons: Dict[OdooSeries, Set[str]] = {
    OdooSeries.v8_0: (
        _core_addons_ce[OdooSeries.v9_0] | _core_addons_ee[OdooSeries.v9_0]
    ),
    OdooSeries.v9_0: (
        _core_addons_ce[OdooSeries.v9_0] | _core_addons_ee[OdooSeries.v9_0]
    ),
    OdooSeries.v10_0: (
        _core_addons_ce[OdooSeries.v10_0] | _core_addons_ee[OdooSeries.v10_0]
    ),
    OdooSeries.v11_0: (
        _core_addons_ce[OdooSeries.v11_0] | _core_addons_ee[OdooSeries.v11_0]
    ),
    OdooSeries.v12_0: (
        _core_addons_ce[OdooSeries.v12_0] | _core_addons_ee[OdooSeries.v12_0]
    ),
    OdooSeries.v13_0: (
        _core_addons_ce[OdooSeries.v13_0] | _core_addons_ee[OdooSeries.v13_0]
    ),
    OdooSeries.v14_0: (
        _core_addons_ce[OdooSeries.v14_0] | _core_addons_ee[OdooSeries.v14_0]
    ),
}


def is_core_addon(addon_name: str, odoo_series: OdooSeries) -> bool:
    return addon_name in _core_addons[odoo_series]


def get_core_addons(odoo_series: OdooSeries) -> Iterable[str]:
    return _core_addons[odoo_series]
