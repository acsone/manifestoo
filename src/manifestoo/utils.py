import sys
from typing import Iterable, List, Optional

import typer

from . import echo


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


def notice_or_abort(msg: str, abort: bool) -> None:
    if abort:
        echo.error(msg)
        raise typer.Abort()
    else:
        echo.notice(msg)
