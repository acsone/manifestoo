import typer

verbosity = 0


def debug(msg: str) -> None:
    if verbosity > 1:
        typer.secho(msg, dim=True, err=True)


def info(msg: str, nl: bool = True) -> None:
    if verbosity > 0:
        typer.secho(msg, fg=typer.colors.BRIGHT_BLUE, err=True, nl=nl)


def notice(msg: str, nl: bool = True) -> None:
    if verbosity > -1:
        typer.secho(msg, fg=typer.colors.GREEN, err=True, nl=nl)


def warning(msg: str) -> None:
    if verbosity > -2:
        typer.secho(msg, fg=typer.colors.YELLOW, err=True)


def error(msg: str) -> None:
    typer.secho(msg, fg=typer.colors.RED, err=True)
