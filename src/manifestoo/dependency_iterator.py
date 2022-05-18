from typing import Iterable, Iterator, Optional, Set, Tuple

from manifestoo_core.addon import Addon
from manifestoo_core.addons_set import AddonsSet

from .addons_selection import AddonsSelection


def dependency_iterator(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    transitive: bool,
) -> Iterator[Tuple[str, Optional[Addon]]]:
    """Iterate addons and their dependencies.

    Yield tuples:
    - addon name
    - addon object (None if not found in addons_set)

    If transitive is False, only yield addon_selection.

    An addon is yielded at most once.
    """
    done: Set[str] = set()

    def _iter(
        addon_names: Iterable[str],
    ) -> Iterator[Tuple[str, Optional[Addon]]]:
        done.update(addon_names)
        for addon_name in addon_names:
            addon = addons_set.get(addon_name)
            yield addon_name, addon
            if transitive and addon:
                yield from _iter(set(addon.manifest.depends) - done)

    yield from _iter(addons_selection)
