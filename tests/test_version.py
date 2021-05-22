from typer.testing import CliRunner

from manifestoo.main import app
from manifestoo.version import __version__

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"manifestoo version {__version__}\n"
