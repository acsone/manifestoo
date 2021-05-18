from typing import Optional

import typer

verbosity = 0


def debug(msg: str) -> None:
    if verbosity > 1:
        typer.secho(msg, dim=True, err=True)


def info(
    msg: str, nl: bool = True, bold: bool = False, bold_intro: Optional[str] = None
) -> None:
    if verbosity > 0:
        if bold_intro:
            typer.secho(
                bold_intro, fg=typer.colors.BRIGHT_BLUE, err=True, nl=False, bold=True
            )
        typer.secho(msg, fg=typer.colors.BRIGHT_BLUE, err=True, nl=nl, bold=bold)


def notice(msg: str, nl: bool = True, bold: bool = False) -> None:
    if verbosity > -1:
        typer.secho(msg, fg=typer.colors.GREEN, err=True, nl=nl, bold=bold)


def warning(msg: str) -> None:
    if verbosity > -2:
        typer.secho(msg, fg=typer.colors.YELLOW, err=True)


def error(msg: str, err: bool = True) -> None:
    typer.secho(msg, fg=typer.colors.RED, err=err)
