import sys
from pathlib import Path

from .manifest import InvalidManifest, Manifest, ManifestDict

if sys.version_info >= (3, 8):
    from typing import TypedDict

    class AddonDict(TypedDict):
        manifest: ManifestDict
        manifest_path: str
        path: str


else:
    from typing import Any, Dict

    AddonDict = Dict[str, Any]


class AddonNotFound(Exception):
    pass


class AddonNotFoundNotInstallable(AddonNotFound):
    pass


class AddonNotFoundNoManifest(AddonNotFound):
    pass


class AddonNotFoundNotADirectory(AddonNotFound):
    pass


class AddonNotFoundInvalidManifest(AddonNotFound):
    pass


def _get_manifest_path(addon_dir: Path) -> Path:
    for manifest_name in ("__manifest__.py", "__openerp__.py", "__terp__.py"):
        manifest_path = addon_dir / manifest_name
        if manifest_path.is_file():
            return manifest_path
    raise AddonNotFoundNoManifest(f"No manifest found in {addon_dir}")


class Addon:
    def __init__(self, manifest: Manifest):
        self.manifest = manifest
        self.manifest_path = manifest.manifest_path
        self.path = self.manifest_path.parent
        self.name = self.path.name

    @classmethod
    def from_addon_dir(
        cls, addon_dir: Path, allow_not_installable: bool = False
    ) -> "Addon":
        if not addon_dir.is_dir():
            raise AddonNotFoundNotADirectory(f"{addon_dir} is not a directory")
        manifest_path = _get_manifest_path(addon_dir)
        try:
            manifest = Manifest.from_manifest_path(manifest_path)
            if not allow_not_installable and not manifest.installable:
                raise AddonNotFoundNotInstallable(f"{addon_dir} is not installable")
        except InvalidManifest as e:
            raise AddonNotFoundInvalidManifest(str(e)) from e
        return cls(manifest)

    def as_dict(self) -> AddonDict:
        """Convert to a dictionary suitable for json output."""
        return dict(
            manifest=self.manifest.manifest_dict,
            manifest_path=str(self.manifest_path),
            path=str(self.path),
        )
