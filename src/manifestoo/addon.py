import ast
from pathlib import Path

from .manifest import Manifest


class AddonNotFound(Exception):
    pass


class AddonNotInstallable(AddonNotFound):
    pass


class NoManifestFound(AddonNotFound):
    pass


class NotADirectory(AddonNotFound):
    pass


class InvalidManifest(AddonNotFound):
    pass


def _get_manifest_path(addon_dir: Path) -> Path:
    for manifest_name in ("__manifest__.py", "__openerp__.py", "__terp__.py"):
        manifest_path = addon_dir / manifest_name
        if manifest_path.is_file():
            return manifest_path
    raise NoManifestFound(f"No manifest found in {addon_dir}")


def _read_manifest(path: Path) -> Manifest:
    try:
        manifest = ast.literal_eval(path.read_text())
    except SyntaxError as e:
        raise InvalidManifest(f"Manifest {path} is invalid: {e}")
    else:
        if not isinstance(manifest, dict):
            raise InvalidManifest(f"Manifest {path} is not a dictionary")
        return Manifest(path, manifest)


class Addon:
    def __init__(self, manifest: Manifest, manifest_path: Path):
        assert manifest._manifest_path == manifest_path
        self.manifest = manifest
        self.manifest_path = manifest_path
        self.path = manifest_path.parent
        self.name = self.path.name

    @classmethod
    def from_addon_dir(
        cls, addon_dir: Path, allow_not_installable: bool = False
    ) -> "Addon":
        if not addon_dir.is_dir():
            raise NotADirectory(f"{addon_dir} is not a directory")
        manifest_path = _get_manifest_path(addon_dir)
        manifest = _read_manifest(manifest_path)
        if not manifest.installable and not allow_not_installable:
            raise AddonNotInstallable(f"{addon_dir} is not installable")
        return cls(manifest, manifest_path)
