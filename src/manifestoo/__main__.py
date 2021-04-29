import typer

app = typer.Typer()


class MainOptions:
    include: str
    exclude: str


@app.callback()
def callback(
    ctx: typer.Context,
    addons_paths: str = typer.Option(
        "",
    ),
    addons_paths_from_odoo_rc: bool = typer.Option(
        False,
        help=(
            "Expand addons paths by looking into the Odoo configuration file "
            "found at $ODOO_RC, if present."
        ),
    ),
    addons_paths_from_odoo: bool = typer.Option(
        False,
        help=(
            "Expand addons paths by trying to 'import odoo' and "
            "looking at 'odoo.addons.__path__'."
        ),
    ),
    include: str = typer.Option(
        "",
        metavar="addon1,addon2,...",
        help=(
            "Comma separated list of addons to include (default: all "
            "installable addons found in --addons-dir')."
        ),
    ),
    exclude: str = typer.Option(
        "",
        metavar="addon1,addon2,...",
        help=("Comma separated list of addons to exclude."),
    ),
    ignore_missing_dependencies: bool = typer.Option(
        False,
        help=("Do not fail if dependencies are missing."),
    ),
) -> None:
    """Do things with addons lists.

    Main options of this command select addons on which the subcommands will
    act. Run 'moo <subcommand> --help' for more options.
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
def check_licences() -> None:
    """Check that selected addons only depend on addons with compatible licences."""
    raise NotImplementedError()


@app.command()
def check_dev_status() -> None:
    """Check that selected addons only depend on addons that have an equal or
    higher development status."""
    raise NotImplementedError()


@app.command()
def tree() -> None:
    """Print a dependency tree of Odoo addons."""
    raise NotImplementedError()


def main() -> None:
    app(obj=MainOptions())


if __name__ == "__main__":
    main()
