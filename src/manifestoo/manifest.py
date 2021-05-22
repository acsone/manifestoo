import ast
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar

T = TypeVar("T")
VT = TypeVar("VT")


def _check_str(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError()
    return value


def _check_optional_str(value: Any) -> Optional[str]:
    if value is None:
        return value
    return _check_str(value)


def _check_bool(value: Any) -> bool:
    if not isinstance(value, bool):
        raise TypeError()
    return value


def _check_list(value: Any, item_checker: Callable[[Any], T]) -> List[T]:
    if not isinstance(value, list):
        raise TypeError()
    map(item_checker, value)
    return value


def _check_dict(
    value: Any, key_checker: Callable[[Any], T], value_checker: Callable[[Any], VT]
) -> Dict[T, VT]:
    if not isinstance(value, dict):
        raise TypeError()
    for k, v in value.items():
        key_checker(k)
        value_checker(v)
    return value


def _check_list_of_str(value: Any) -> List[str]:
    # this could be a partial but mypy does not support it
    return _check_list(value, item_checker=_check_str)


def _check_dict_of_list_of_str(value: Any) -> Dict[str, List[str]]:
    # this could be a partial but mypy does not support it
    return _check_dict(value, key_checker=_check_str, value_checker=_check_list_of_str)


class InvalidManifest(Exception):
    pass


class Manifest:
    def __init__(self, manifest_path: Path, manifest_dict: Dict[Any, Any]) -> None:
        self.manifest_path = manifest_path
        self.manifest_dict = manifest_dict

    @classmethod
    def from_manifest_path(cls, manifest_path: Path) -> "Manifest":
        try:
            manifest = ast.literal_eval(manifest_path.read_text())
        except SyntaxError as e:
            raise InvalidManifest(f"Manifest {manifest_path} is invalid: {e}")
        else:
            if not isinstance(manifest, dict):
                raise InvalidManifest(f"Manifest {manifest_path} is not a dictionary")
            return Manifest(manifest_path, manifest)

    def _get(self, key: str, checker: Callable[[Any], T], default: T) -> T:
        """Get value with runtime type check."""
        try:
            value = self.manifest_dict[key]
        except KeyError:
            return default
        try:
            return checker(value)
        except TypeError:
            raise InvalidManifest(
                f"{value!r} has invalid type for {key!r} in {self.manifest_path}"
            )

    @property
    def name(self) -> Optional[str]:
        return self._get("name", _check_optional_str, default=None)

    @property
    def version(self) -> Optional[str]:
        return self._get("version", _check_optional_str, default=None)

    @property
    def installable(self) -> bool:
        return self._get("installable", _check_bool, default=True)

    @property
    def depends(self) -> List[str]:
        return self._get("depends", _check_list_of_str, default=[])

    @property
    def external_dependencies(self) -> Dict[str, List[str]]:
        return self._get(
            "external_dependencies", _check_dict_of_list_of_str, default={}
        )

    @property
    def license(self) -> Optional[str]:
        return self._get("license", _check_optional_str, default=None)

    @property
    def development_status(self) -> Optional[str]:
        return self._get("development_status", _check_optional_str, default=None)
