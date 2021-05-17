from enum import Enum
from pathlib import Path
from typing import List, Optional

import typer

from . import echo

__version__ = "0.1"

app = typer.Typer()


class MainOptions:
    select: str
    exclude: str


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
            "Select all addons found in this directory. "
            "This option may be repeated. "
            "The directories selected with this options are "
            "automatically added to the addons search path."
        ),
        show_default=False,
    ),
    select: Optional[str] = typer.Option(
        None,
        metavar="addon1,addon2,...",
        help=(
            "Comma separated list of addons to select. "
            "These addons will be searched in the addons path."
        ),
    ),
    select_core_ce_addons: Optional[OdooSeries] = typer.Option(
        None,
    ),
    select_core_ee_addons: Optional[OdooSeries] = typer.Option(
        None,
    ),
    select_exclude: Optional[str] = typer.Option(
        None,
        metavar="addon1,addon2,...",
        help=(
            "Comma separated list of addons to exclude from selection. "
            "This option is useful in combination with --select-addons-dir."
        ),
    ),
    addons_path: Optional[str] = typer.Option(
        None,
        help="Expand addons path with this comma separated list of directories.",
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
    addons_path_from_import_odoo: bool = typer.Option(
        True,
        help=(
            "Expand addons path by trying to `import odoo` and "
            "looking at `odoo.addons.__path__`. This option is useful when "
            "addons have been installed with pip."
        ),
    ),
    python: str = typer.Option(
        "python",
        "--python",
        "-p",
        show_default=False,
        metavar="PYTHON",
        help=(
            "The python executable to use. when importing `odoo.addons.__path__`. "
            "Defaults to the 'python' executable found in PATH."
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
        "--quier",
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


@app.command()
def list() -> None:
    """Print the selected addons."""
    raise NotImplementedError()


@app.command()
def list_depends(
    recursive: bool = False,
    include_selected: bool = typer.Option(
        False,
        help="Whether to print the selected addons along with their dependencies.",
    ),
    as_pip_requirements: bool = False,
) -> None:
    """Print the dependencies of selected addons."""
    raise NotImplementedError()


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
    raise NotImplementedError()


@app.command()
def check_licences(
    recursive: bool = True,
) -> None:
    """Check licenses.

    Check that selected addons only depend on addons with compatible
    licences.
    """
    raise NotImplementedError()


@app.command()
def check_dev_status(
    recursive: bool = True,
) -> None:
    """Check development status.

    Check that selected addons only depend on addons that have an equal
    or higher development status.
    """
    raise NotImplementedError()


@app.command()
def tree() -> None:
    """Print the dependency tree of selected addons."""
    raise NotImplementedError()


def main() -> None:
    app(obj=MainOptions())


if __name__ == "__main__":
    main()
