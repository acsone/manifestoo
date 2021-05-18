from typing import Iterable

from ..addons_selection import AddonsSelection


def list_command(addons_selection: AddonsSelection) -> Iterable[str]:
    return sorted(addons_selection)
