import json
import sys
from typing import Any, Dict, Iterable, List, Optional

import typer

from . import echo
from .addon import AddonDict
from .addons_set import AddonsSet
from .odoo_series import OdooSeries


def comma_split(s: Optional[str]) -> List[str]:
    if not s:
        return []
    s = s.strip()
    if not s:
        return []
    items = [item.strip() for item in s.split(",")]
    return [item for item in items if item]


def not_implemented(what: str) -> None:
    echo.error(f"{what} is not implemented.")
    raise typer.Abort()


def print_list(lst: Iterable[str], separator: str) -> None:
    if not lst:
        return
    sys.stdout.write(separator.join(lst))
    sys.stdout.write("\n")


def print_json(obj: Any) -> None:
    json.dump(obj, sys.stdout)
    sys.stdout.write("\n")


def print_addons_as_json(names: Iterable[str], addons_set: AddonsSet) -> None:
    d: Dict[str, Optional[AddonDict]] = {}
    for name in names:
        if name in addons_set:
            d[name] = addons_set[name].as_dict()
        else:
            d[name] = None
    print_json(d)


def notice_or_abort(msg: str, abort: bool) -> None:
    if abort:
        echo.error(msg)
        raise typer.Abort()
    else:
        echo.notice(msg)


def ensure_odoo_series(odoo_series: Optional[OdooSeries]) -> None:
    if not odoo_series:
        echo.error(
            "Odoo series could not be detected. Please provide one with --odoo-series."
        )
        raise typer.Abort()
