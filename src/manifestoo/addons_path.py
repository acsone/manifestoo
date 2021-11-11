import ast
import os
import subprocess
import tempfile
from configparser import ConfigParser
from pathlib import Path
from typing import Iterable, List

from . import echo
from .utils import comma_split

ADDONS_PATH_SCRIPT = b"""\
import sys
try:
    import openerp as odoo
except ImportError:
    import odoo

odoo.modules.initialize_sys_path()

if odoo.release.version_info >= (13, ):
    path = odoo.addons.__path__
else:
    path = odoo.modules.module.ad_paths

with open(sys.argv[1], "wb") as f:
    f.write(repr(path).encode("utf-8"))
"""


class AddonsPath(List[Path]):
    def __str__(self) -> str:
        return ",".join(str(item) for item in self)

    def extend_from_addons_dirs(self, addons_dirs: Iterable[Path]) -> None:
        self.extend(addons_dirs)

    def extend_from_addons_path(self, addons_path: str) -> None:
        return self.extend(Path(item) for item in comma_split(addons_path))

    def extend_from_odoo_cfg(self, odoo_cfg_path: Path) -> None:
        config = ConfigParser()
        config.read(odoo_cfg_path)
        addons_path = config.get("options", "addons_path", fallback=None)
        if not addons_path:
            return None
        self.extend_from_addons_path(addons_path)

    def extend_from_import_odoo(self, python: str) -> None:
        script = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
        try:
            script.write(ADDONS_PATH_SCRIPT)
            script.close()
            output = tempfile.NamedTemporaryFile(delete=False)
            try:
                output.close()
                try:
                    r = subprocess.call(
                        [python, script.name, output.name],
                        stderr=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        env=os.environ,
                    )
                except FileNotFoundError:
                    # python not found
                    r = 1
                if r != 0:
                    echo.notice(f"could not obtain odoo.addons.__path__ using {python}")
                    return
                addons_paths = ast.literal_eval(Path(output.name).read_text())
                self.extend(Path(item) for item in addons_paths)
            finally:
                os.unlink(output.name)
        finally:
            os.unlink(script.name)
