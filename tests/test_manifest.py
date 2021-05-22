import pytest

from manifestoo.manifest import InvalidManifest

from .common import mock_manifest


@pytest.mark.parametrize(
    "key, value",
    [
        ("name", "the name"),
        ("name", None),
        ("version", "1.0.0"),
        ("version", None),
        ("license", "GPL-3"),
        ("license", None),
        ("development_status", "Beta"),
        ("development_status", None),
        ("depends", ["a", "b"]),
        ("external_dependencies", {"python": ["httpx"]}),
        ("installable", True),
        ("installable", False),
    ],
)
def test_manifest_valid_value(key, value):
    manifest = mock_manifest({key: value})
    assert getattr(manifest, key) == value


@pytest.mark.parametrize(
    "key, value",
    [
        ("name", 1),
        ("version", 1),
        ("license", ["i"]),
        ("development_status", {}),
        ("depends", 1),
        ("depends", {}),
        ("depends", None),
        ("external_dependencies", {1: {}}),
        ("external_dependencies", None),
        ("external_dependencies", [1]),
        ("installable", 1),
        ("installable", None),
    ],
)
def test_manifest_invalid_value(key, value):
    manifest = mock_manifest({key: value})
    with pytest.raises(InvalidManifest):
        getattr(manifest, key)


@pytest.mark.parametrize(
    "key, default",
    [
        ("name", None),
        ("version", None),
        ("license", None),
        ("development_status", None),
        ("depends", []),
        ("external_dependencies", {}),
        ("installable", True),
    ],
)
def test_manifest_default_value(key, default):
    manifest = mock_manifest({})
    assert getattr(manifest, key) == default
