from enum import Enum
from pathlib import Path
from typing import List, Optional

import typer

from . import echo
from .commands.list import list_command
from .commands.list_depends import list_depends_command
from .options import MainOptions
from .utils import not_implemented, print_list

__version__ = "0.1"

app = typer.Typer()


class OdooSeries(str, Enum):
    v8 = "8.0"
    v9 = "9.0"
    v10 = "10.0"
    v11 = "11.0"
    v12 = "12.0"
    v13 = "13.0"
    v14 = "14.0"


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"manifestoo version {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    ctx: typer.Context,
    select_addons_dirs: Optional[List[Path]] = typer.Option(
        None,
        "--select-addons-dir",
        "-d",
        exists=True,
        file_okay=False,
        dir_okay=True,
        help=(
            "Select all installable addons found in this directory. "
            "This option may be repeated. "
            "The directories selected with this options are "
            "automatically added to the addons search path."
        ),
        show_default=False,
    ),
    select_include: Optional[str] = typer.Option(
        None,
        metavar="addon1,addon2,...",
        help=(
            "Comma separated list of addons to select. "
            "These addons will be searched in the addons path."
        ),
    ),
    select_exclude: Optional[str] = typer.Option(
        None,
        metavar="addon1,addon2,...",
        help=(
            "Comma separated list of addons to exclude from selection. "
            "This option is useful in combination with --select-addons-dir."
        ),
    ),
    select_core_ce_addons: Optional[OdooSeries] = typer.Option(
        None,
    ),
    select_core_ee_addons: Optional[OdooSeries] = typer.Option(
        None,
    ),
    addons_path: Optional[str] = typer.Option(
        None,
        help="Expand addons path with this comma separated list of directories.",
    ),
    addons_path_from_import_odoo: bool = typer.Option(
        True,
        help=(
            "Expand addons path by trying to `import odoo` and "
            "looking at `odoo.addons.__path__`. This option is useful when "
            "addons have been installed with pip."
        ),
    ),
    addons_path_python: str = typer.Option(
        "python",
        "--addons-path-python",
        show_default=False,
        metavar="PYTHON",
        help=(
            "The python executable to use. when importing `odoo.addons.__path__`. "
            "Defaults to the 'python' executable found in PATH."
        ),
    ),
    addons_path_from_odoo_cfg: Optional[Path] = typer.Option(
        None,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        envvar="ODOO_RC",
        help=(
            "Expand addons path by looking into the provided Odoo configuration file. "
        ),
    ),
    separator: str = typer.Option(
        default="\n",
        show_default=False,
        help="Separator charater to use (by default, print one item per line).",
    ),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        show_default=False,
    ),
    quiet: int = typer.Option(
        0,
        "--quiet",
        "-q",
        count=True,
        show_default=False,
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Do things with Odoo addons lists.

    The main options of this command select addons on which the subcommands
    will act. The --addons-path options provide locations to search for addons.

    Run `manifestoo <subcommand> --help` for more options.
    """
    echo.verbosity += verbose
    echo.verbosity -= quiet
    main_options = MainOptions()
    main_options.separator = separator
    # resolve addons_path
    if select_addons_dirs:
        main_options.addons_path.extend_from_addons_dirs(select_addons_dirs)
    if addons_path:
        main_options.addons_path.extend_from_addons_path(addons_path)
    if addons_path_from_import_odoo:
        main_options.addons_path.extend_from_import_odoo(addons_path_python)
    if addons_path_from_odoo_cfg:
        main_options.addons_path.extend_from_odoo_cfg(addons_path_from_odoo_cfg)
    echo.info(str(main_options.addons_path), bold_intro="Addons path: ")
    # populate addons_set
    main_options.addons_set.add_from_addons_dirs(main_options.addons_path)
    echo.info(str(main_options.addons_set), bold_intro="Addons set: ")
    # addons selection
    if select_addons_dirs:
        main_options.addons_selection.add_addons_dirs(select_addons_dirs)
    if select_include:
        main_options.addons_selection.add_addon_names(select_include)
    if select_exclude:
        main_options.addons_selection.remove_addon_names(select_exclude)
    if select_core_ce_addons:
        not_implemented("--select-core-ce-addons")
    if select_core_ee_addons:
        not_implemented("--select-core-ee-addons")
    echo.info(str(main_options.addons_selection), bold_intro="Addons selection: ")
    # pass main options to commands
    ctx.obj = main_options


@app.command()
def list(ctx: typer.Context) -> None:
    """Print the selected addons."""
    main_options: MainOptions = ctx.obj
    result = list_command(main_options.addons_selection)
    print_list(result, ctx.obj.separator)


@app.command()
def list_depends(
    ctx: typer.Context,
    recursive: bool = typer.Option(
        False,
        "--recursive",
        help="Recursively print dependencies.",
        show_default=False,
    ),
    include_selected: bool = typer.Option(
        False,
        "--include-selected",
        help="Print the selected addons along with their dependencies.",
        show_default=False,
    ),
    ignore_missing: bool = typer.Option(
        False,
        "--ignore-missing",
        help=(
            "Do not fail if dependencies are not found in addons path. "
            "This only applies to top level (selected) addons "
            "and recursive dependencies."
        ),
        show_default=False,
    ),
    as_pip_requirements: bool = typer.Option(
        False,
        "--as-pip-requirements",
        show_default=False,
    ),
) -> None:
    """Print the dependencies of selected addons."""
    main_options: MainOptions = ctx.obj
    if as_pip_requirements:
        not_implemented("--as-pip-requirement")
    result, missing = list_depends_command(
        main_options.addons_selection,
        main_options.addons_set,
        recursive,
        include_selected,
    )
    if missing and not ignore_missing:
        echo.error("not found in addons path: " + ",".join(sorted(missing)))
        raise typer.Abort()
    print_list(
        result,
        ctx.obj.separator,
    )


@app.command()
def list_external_dependencies(
    kind: str = typer.Argument(
        ...,
        help="Kind of external dependency, such as 'python' or 'deb'.",
    ),
    recursive: bool = typer.Option(
        False,
        help=(
            "Whether to print external dependencies of dependant addons. "
            "By default, print only external dependencies of addons selected "
            "with select/exclude."
        ),
    ),
) -> None:
    """Print the external dependencies of selected addons."""
    not_implemented("list-external-dependencies command")


@app.command()
def check_licenses(
    recursive: bool = True,
) -> None:
    """Check licenses.

    Check that selected addons only depend on addons with compatible
    licenses.
    """
    not_implemented("check-license command")


@app.command()
def check_dev_status(
    recursive: bool = True,
) -> None:
    """Check development status.

    Check that selected addons only depend on addons that have an equal
    or higher development status.
    """
    not_implemented("check-dev-status command")


@app.command()
def tree() -> None:
    """Print the dependency tree of selected addons."""
    not_implemented("tree command")


def main() -> None:
    app(obj=MainOptions())


if __name__ == "__main__":
    main()
