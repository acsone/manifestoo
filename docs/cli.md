# `manifestoo`

Reason about Odoo addons manifests.

The `--select-*` options of this command select addons on which the
subcommands will act. The `--addons-path` options provide locations to
search for addons.

Run `manifestoo <subcommand> --help` for more options.

**Usage**:

```console
$ manifestoo [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-d, --select-addons-dir DIRECTORY`: Select all installable addons found in this directory. This option may be repeated. The directories selected with this options are automatically added to the addons search path.
* `--select-include, --select addon1,addon2,...`: Comma separated list of addons to select. These addons will be searched in the addons path.
* `--select-exclude addon1,addon2,...`: Comma separated list of addons to exclude from selection. This option is useful in combination with `--select-addons-dir`.
* `--select-core-addons`: Select the Odoo core addons (CE and EE) for the given series.
* `--addons-path TEXT`: Expand addons path with this comma separated list of directories.
* `--addons-path-from-import-odoo / --no-addons-path-from-import-odoo`: Expand addons path by trying to `import odoo` and looking at `odoo.addons.__path__`. This option is useful when addons have been installed with pip.  [default: True]
* `--addons-path-python PYTHON`: The python executable to use when importing `odoo.addons.__path__`. Defaults to the `python` executable found in PATH.
* `--addons-path-from-odoo-cfg FILE`: Expand addons path by looking into the provided Odoo configuration file.   [env var: ODOO_RC]
* `--odoo-series [8.0|9.0|10.0|11.0|12.0|13.0|14.0]`: Odoo series to use, in case it is not autodetected from addons version.  [env var: ODOO_VERSION, ODOO_SERIES]
* `-v, --verbose`
* `-q, --quiet`
* `--version`
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `check-dev-status`: Check development status compatibility.
* `check-licenses`: Check license compatibility.
* `list`: Print the selected addons.
* `list-depends`: Print the dependencies of selected addons.
* `list-external-dependencies`: Print the external dependencies of selected...
* `tree`: Print the dependency tree of selected addons.

## `manifestoo check-dev-status`

Check development status compatibility.

Check that selected addons only depend on addons that have an equal
or higher development status.

**Usage**:

```console
$ manifestoo check-dev-status [OPTIONS]
```

**Options**:

* `--transitive`: Also check transitive dependencies.
* `--default-dev-status TEXT`
* `--help`: Show this message and exit.

## `manifestoo check-licenses`

Check license compatibility.

Check that selected addons only depend on addons with compatible
licenses.

**Usage**:

```console
$ manifestoo check-licenses [OPTIONS]
```

**Options**:

* `--transitive`: Also check transitive dependencies.
* `--help`: Show this message and exit.

## `manifestoo list`

Print the selected addons.

**Usage**:

```console
$ manifestoo list [OPTIONS]
```

**Options**:

* `--separator TEXT`: Separator charater to use (by default, print one item per line).
* `--help`: Show this message and exit.

## `manifestoo list-depends`

Print the dependencies of selected addons.

**Usage**:

```console
$ manifestoo list-depends [OPTIONS]
```

**Options**:

* `--separator TEXT`: Separator charater to use (by default, print one item per line).
* `--transitive`: Print all transitive dependencies.
* `--include-selected`: Print the selected addons along with their dependencies.
* `--ignore-missing`: Do not fail if dependencies are not found in addons path. This only applies to top level (selected) addons and transitive dependencies.
* `--as-pip-requirements`
* `--help`: Show this message and exit.

## `manifestoo list-external-dependencies`

Print the external dependencies of selected addons.

**Usage**:

```console
$ manifestoo list-external-dependencies [OPTIONS] KIND
```

**Arguments**:

* `KIND`: Kind of external dependency, such as `python` or `deb`.  [required]

**Options**:

* `--separator TEXT`: Separator charater to use (by default, print one item per line).
* `--transitive`: Print external dependencies of all transitive dependent addons.
* `--ignore-missing`: Do not fail if dependencies are not found in addons path. This only applies to top level (selected) addons and transitive dependencies.
* `--help`: Show this message and exit.

## `manifestoo tree`

Print the dependency tree of selected addons.

**Usage**:

```console
$ manifestoo tree [OPTIONS]
```

**Options**:

* `--fold-core-addons`: Do not expand dependencies of core Odoo addons.
* `--help`: Show this message and exit.
