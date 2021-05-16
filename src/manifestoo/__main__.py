import sys
from enum import Enum
from pathlib import Path
from typing import List, Optional

import typer

from manifestoo.addon import NotADirectory

app = typer.Typer()


class MainOptions:
    include: str
    exclude: str


class OdooSeries(str, Enum):
    v8 = "8.0"
    v9 = "9.0"
    v10 = "10.0"
    v11 = "11.0"
    v12 = "12.0"
    v13 = "13.0"
    v14 = "14.0"


@app.callback()
def callback(
    ctx: typer.Context,
    include_addons_dirs: List[Path] = typer.Option(
        [],
        "--include-addons-dir",
        exists=True,
        file_okay=False,
        dir_okay=True,
        help=(
            "Include all addons found in this directory. "
            "This option may be repeated. "
            "The directories selected with this options are "
            "automatically added to the addons search path."
        ),
        show_default=False,
    ),
    include: Optional[str] = typer.Option(
        None,
        metavar="addon1,addon2,...",
        help=(
            "Comma separated list of addons to include. "
            "These addons will be searched in the addons path."
        ),
    ),
    include_core_ce_addons: Optional[OdooSeries] = typer.Option(
        None,
    ),
    include_core_ee_addons: Optional[OdooSeries] = typer.Option(
        None,
    ),
    exclude: Optional[str] = typer.Option(
        None,
        metavar="addon1,addon2,...",
        help=(
            "Comma separated list of addons to exclude. "
            "This option is useful in combination with --include-addons-dirs."
        ),
    ),
    addons_path: Optional[str] = typer.Option(
        None,
        help="Expand addons path with this comma separated list of directories.",
    ),
    addons_path_from_odoo_rc: bool = typer.Option(
        True,
        help=(
            "Expand addons path by looking into the Odoo configuration file "
            "found at $ODOO_RC, if present."
        ),
    ),
    addons_path_from_odoo_cfg: Optional[Path] = typer.Option(
        None,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help=(
            "Expand addons path by looking into the provided Odoo configuration file."
        ),
    ),
    addons_path_from_import_odoo: bool = typer.Option(
        False,
        help=(
            "Expand addons path by trying to 'import odoo' and "
            "looking at 'odoo.addons.__path__'. This option is useful when "
            "addons have been installed with pip."
        ),
    ),
    python: Path = typer.Option(
        Path(sys.executable),
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help=("Python executable to use when importing 'odoo.addons.__path__'."),
    ),
    separator: str = typer.Option(
        default="\n",
        show_default=False,
        help="Separator charater to use (by default, print one item per line).",
    ),
    verbose: bool = typer.Option(
        False,
    ),
) -> None:
    """Do things with addons lists.

    The main options of this command select addons on which the subcommands
    will act. Options starting with --include and --exclude are used to select
    top level addons to work on. The --addons-path options provide locations to
    search for addons.

    Run 'moo <subcommand> --help' for more options.
    """
    pass


@app.command()
def list() -> None:
    """Print the selected addons."""
    raise NotImplementedError()


@app.command()
def list_depends() -> None:
    """Print the direct dependencies of selected addons."""
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
            "with include/exclude."
        ),
    ),
) -> None:
    """Print the external dependencies of selected addons."""
    raise NotImplementedError()


@app.command()
def check_licences() -> None:
    """Check that selected addons only depend on addons with compatible licences."""
    raise NotImplementedError()


@app.command()
def check_dev_status() -> None:
    """Check that selected addons only depend on addons that have an equal or higher
    development status."""
    raise NotImplementedError()


@app.command()
def tree() -> None:
    """Print the dependency tree of addons selected with include/exclude options."""
    raise NotImplementedError()


def main() -> None:
    app(obj=MainOptions())


if __name__ == "__main__":
    main()
