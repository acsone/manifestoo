import os
import ast
import subprocess
from pathlib import Path
from configparser import ConfigParser
from typing import Sequence, Iterable
import tempfile


def _from_addons_paths(addons_paths: Iterable[str]) -> Sequence[Path]:
    return [Path(item.strip()) for item in addons_paths]


def from_addons_path(addons_path: str) -> Sequence[Path]:
    return _from_addons_paths(addons_path.split(","))


def from_odoo_rc(odoo_rc_path: Path) -> Sequence[Path]:
    config = ConfigParser()
    config.read(odoo_rc_path)
    addons_path = config.get("options", "addons_path", fallback=None)
    if not addons_path:
        return []
    return from_addons_path(addons_path)


ADDONS_PATH_SCRIPT = b"""\
import sys
try:
    import openerp as odoo
except ImportError:
    import odoo

with open(sys.argv[1], "wb") as f:
    f.write(repr(odoo.addons.__path__).encode("utf-8"))
"""


def from_import_odoo(python: str) -> Sequence[Path]:
    script = tempfile.NamedTemporaryFile(delete=False)
    try:
        script.write(ADDONS_PATH_SCRIPT)
        script.close()
        output = tempfile.NamedTemporaryFile(delete=False)
        try:
            output.close()
            r = subprocess.call(
                [python, script.name, output.name],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
            if r != 0:
                return []
            addons_paths = ast.literal_eval(Path(output.name).read_text())
            return _from_addons_paths(addons_paths)
        finally:
            os.unlink(output.name)
    finally:
        os.unlink(script.name)
