# `manifestoo`

Do things with Odoo addons lists.

The main options of this command select addons on which the subcommands
will act. Options starting with --select and --exclude are used to select
top level addons on which subcommands will act. The --addons-path options
provide locations to search for addons.

Run 'moo <subcommand> --help' for more options.

**Usage**:

```console
$ manifestoo [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-d, --select-addons-dir DIRECTORY`: Select all addons found in this directory. This option may be repeated. The directories selected with this options are automatically added to the addons search path.
* `--select addon1,addon2,...`: Comma separated list of addons to select. These addons will be searched in the addons path.
* `--select-core-ce-addons [8.0|9.0|10.0|11.0|12.0|13.0|14.0]`
* `--select-core-ee-addons [8.0|9.0|10.0|11.0|12.0|13.0|14.0]`
* `--exclude addon1,addon2,...`: Comma separated list of addons to exclude. This option is useful in combination with --select-addons-dirs.
* `--addons-path TEXT`: Expand addons path with this comma separated list of directories.
* `--addons-path-from-odoo-cfg FILE`: Expand addons path by looking into the provided Odoo configuration file.   [env var: ODOO_RC]
* `--addons-path-from-import-odoo / --no-addons-path-from-import-odoo`: Expand addons path by trying to 'import odoo' and looking at `odoo.addons.__path__`. This option is useful when addons have been installed with pip.  [default: True]
* `-p, --python PYTHON`: The python executable to use. when importing `odoo.addons.__path__`. Defaults to the 'python' executable found in PATH.
* `--separator TEXT`: Separator charater to use (by default, print one item per line).
* `--verbose / --no-verbose`: [default: False]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `check-dev-status`: Check development status.
* `check-licences`: Check licenses.
* `list`: Print the selected addons.
* `list-depends`: Print the dependencies of selected addons.
* `list-external-dependencies`: Print the external dependencies of selected...
* `tree`: Print the dependency tree of selected addons.

## `manifestoo check-dev-status`

Check development status.

Check that selected addons only depend on addons that have an equal or
higher development status.

**Usage**:

```console
$ manifestoo check-dev-status [OPTIONS]
```

**Options**:

* `--recursive / --no-recursive`: [default: False]
* `--help`: Show this message and exit.

## `manifestoo check-licences`

Check licenses.

Check that selected addons only depend on addons with compatible licences.

**Usage**:

```console
$ manifestoo check-licences [OPTIONS]
```

**Options**:

* `--recursive / --no-recursive`: [default: False]
* `--help`: Show this message and exit.

## `manifestoo list`

Print the selected addons.

**Usage**:

```console
$ manifestoo list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `manifestoo list-depends`

Print the dependencies of selected addons.

**Usage**:

```console
$ manifestoo list-depends [OPTIONS]
```

**Options**:

* `--recursive / --no-recursive`: [default: False]
* `--as-pip-requirements / --no-as-pip-requirements`: [default: False]
* `--help`: Show this message and exit.

## `manifestoo list-external-dependencies`

Print the external dependencies of selected addons.

**Usage**:

```console
$ manifestoo list-external-dependencies [OPTIONS] KIND
```

**Arguments**:

* `KIND`: Kind of external dependency, such as 'python' or 'deb'.  [required]

**Options**:

* `--recursive / --no-recursive`: Whether to print external dependencies of dependant addons. By default, print only external dependencies of addons selected with select/exclude.  [default: False]
* `--help`: Show this message and exit.

## `manifestoo tree`

Print the dependency tree of selected addons.

**Usage**:

```console
$ manifestoo tree [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

