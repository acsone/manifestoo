import functools
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from manifestoo.addons_selection import AddonsSelection
from manifestoo_core.addon import Addon
from manifestoo_core.addons_set import AddonsSet
from manifestoo_core.manifest import Manifest


def populate_addons_dir(addons_dir: Path, addons: Dict[str, Dict[str, Any]]):
    if not addons_dir.is_dir():
        addons_dir.mkdir()
    for addon_name, manifest in addons.items():
        addon_path = addons_dir / addon_name
        addon_path.mkdir()
        (addon_path / "__init__.py").touch()
        manifest_path = addon_path / "__manifest__.py"
        manifest_path.write_text(repr(manifest))


def mock_addons_set(addons: Dict[str, Dict[str, Any]]) -> AddonsSet:
    addons_set = AddonsSet()
    for addon_name, manifest_dict in addons.items():
        manifest = Manifest.from_dict(manifest_dict)
        manifest_path = Path("/tmp/fake-addons-dir") / addon_name / "__manifest__.py"
        addons_set[addon_name] = Addon(manifest, manifest_path)
    return addons_set


def mock_addons_selection(addon_names: str) -> AddonsSelection:
    addons_selection = AddonsSelection()
    addons_selection.add_addon_names(addon_names)
    return addons_selection


def restore_cwd(function):
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        cwd = os.getcwd()
        try:
            return function(*args, **kwargs)
        finally:
            os.chdir(cwd)

    return decorator


@restore_cwd
def run_in_path(path: Path, function, *args, **kwargs):
    cd_git_root(path)
    return function(*args, **kwargs)


def cd_git_root(git_root: Path):
    os.chdir(git_root)


@restore_cwd
def git_init(git_root: Path):
    cd_git_root(git_root)
    subprocess.check_output(["git", "init"])
    subprocess.check_output(["git", "config", "user.email", "you@example.com"])
    subprocess.check_output(["git", "config", "user.name", "Your Name"])


@restore_cwd
def git_commit(git_root: Path, paths: Optional[Path] = None):
    cd_git_root(git_root)
    paths = paths or ["."]
    subprocess.check_output(["git", "add"] + paths)
    subprocess.check_output(["git", "commit", "-m", "*"])


@restore_cwd
def git_checkout(git_root: Path, branch: str, new: bool = False):
    cd_git_root(git_root)
    command = ["git", "checkout", "-b"] if new else ["git", "checkout"]
    subprocess.check_output(command + [branch])


def modify_addon_file(addon_dir: Path, file_path: Optional[str] = None):
    file_path = file_path or "__manifest__.py"
    with open(addon_dir / file_path, "a") as file_object:
        file_object.write("\n# useless change\n")
