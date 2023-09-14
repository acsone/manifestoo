import pytest
from typer.testing import CliRunner

from manifestoo.git import BranchNotFound, get_branch_modified_addons
from manifestoo.main import app

from .common import (
    git_checkout,
    git_commit,
    git_init,
    modify_addon_file,
    populate_addons_dir,
    run_in_path,
)


def test_git_selection(tmp_path):
    addons_path = tmp_path / "addons"  # this way we can check project files in
    addons = {"a": {"depends": ["b"]}, "b": {}}
    new_addons = {"c": {}}
    git_init(tmp_path)
    populate_addons_dir(addons_path, addons)
    git_commit(tmp_path)
    git_checkout(tmp_path, "develop", new=True)
    populate_addons_dir(addons_path, new_addons)
    git_commit(tmp_path)
    modify_addon_file(addons_path / "b")
    git_commit(tmp_path)

    # now we put things that are NOT in addons to check it does not pollute output
    (tmp_path / ".gitignore").touch()
    git_commit(tmp_path)
    # this one is a bit more tricky:
    (addons_path / "README.md").touch()
    git_commit(tmp_path)

    with pytest.raises(BranchNotFound):  # check it fails on non-existent branch
        run_in_path(tmp_path, get_branch_modified_addons, "main", [addons_path])

    # check get all addons modified on develop branch
    runner = CliRunner(mix_stderr=False)
    result = run_in_path(
        tmp_path,
        runner.invoke,
        app,
        [f"--addons-path={addons_path}", "-g", "master", "list"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0
    assert result.stdout == "b\nc\n"

    # now check we only get new addons
    result = run_in_path(
        tmp_path,
        runner.invoke,
        app,
        [f"--addons-path={addons_path}", "-n", "master", "list"],
        catch_exceptions=False,
    )
    assert not result.exception
    assert result.exit_code == 0
    assert result.stdout == "c\n"
