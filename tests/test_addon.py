from pathlib import Path

import pytest

from manifestoo.addon import (
    Addon,
    AddonNotFoundInvalidManifest,
    AddonNotFoundNoInit,
    AddonNotFoundNoManifest,
    AddonNotFoundNotADirectory,
    AddonNotFoundNotInstallable,
)


@pytest.fixture(
    params=[
        {
            "dir": "a",
            "manifest": "{}",
        }
    ]
)
def addon_dir(request, tmp_path) -> Path:
    addon_dir = tmp_path / request.param["dir"]
    addon_dir.mkdir()
    (addon_dir / "__init__.py").touch()
    (addon_dir / "__manifest__.py").write_text(request.param["manifest"])
    return addon_dir


@pytest.mark.parametrize(
    "addon_dir",
    [
        {
            "dir": "theaddon",
            "manifest": "{'name': 'the addon'}",
        }
    ],
    indirect=True,
)
def test_basic(addon_dir):
    addon = Addon.from_addon_dir(addon_dir)
    assert addon.name == "theaddon"
    assert addon.path == addon_dir
    assert addon.manifest.name == "the addon"


def test_not_a_directory(tmp_path):
    with pytest.raises(AddonNotFoundNotADirectory):
        Addon.from_addon_dir(tmp_path / "not-a-dir")


@pytest.mark.parametrize(
    "addon_dir",
    [
        {
            "dir": "a",
            "manifest": "{'installable': False}",
        }
    ],
    indirect=True,
)
def test_not_installable(addon_dir):
    with pytest.raises(AddonNotFoundNotInstallable):
        Addon.from_addon_dir(addon_dir)
    assert Addon.from_addon_dir(addon_dir, allow_not_installable=True)


@pytest.mark.parametrize(
    "addon_dir",
    [
        {
            "dir": "a",
            "manifest": "[]",
        }
    ],
    indirect=True,
)
def test_invalid_manifest(addon_dir):
    with pytest.raises(AddonNotFoundInvalidManifest):
        Addon.from_addon_dir(addon_dir)


@pytest.mark.parametrize(
    "addon_dir",
    [
        {
            "dir": "a",
            "manifest": "{'installable':}",
        }
    ],
    indirect=True,
)
def test_manifest_syntax_error(addon_dir):
    with pytest.raises(AddonNotFoundInvalidManifest):
        Addon.from_addon_dir(addon_dir)


@pytest.mark.parametrize(
    "addon_dir",
    [
        {
            "dir": "a",
            "manifest": "{'installable': '?'}",
        }
    ],
    indirect=True,
)
def test_manifest_type_error(addon_dir):
    with pytest.raises(AddonNotFoundInvalidManifest):
        Addon.from_addon_dir(addon_dir)


def test_no_manifest(addon_dir):
    (addon_dir / "__manifest__.py").unlink()
    with pytest.raises(AddonNotFoundNoManifest):
        Addon.from_addon_dir(addon_dir)


def test_no_init(addon_dir):
    (addon_dir / "__init__.py").unlink()
    with pytest.raises(AddonNotFoundNoInit):
        Addon.from_addon_dir(addon_dir)
