from typer.testing import CliRunner

from manifestoo.__main__ import __version__, app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"manifestoo version {__version__}\n"
