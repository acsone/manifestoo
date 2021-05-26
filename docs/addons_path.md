# The addons search path

Manifestoo needs to locate the addons you want it to work on, so it can read
their manifest. To this end, there are several mechanism to tell it where to
search for addons.

It has sensible defaults so you don't have to worry about it in common
configurations, yet you have full control via CLI options.

```{tip}
All these mechanisms *extend* the addons path.
```

```{warning}
When the same addon (by name) is present more than once in the addons path,
only one of them will be considered. Which one is unspecified and may change
in the future, so you must not rely on any ordering.

It is highly recommended to avoid having different addons with the same name
in the addons search path.
```

## Selected addons directory

The directory provided with the `--select-addon-dir` option is added to the
addons search path automatically.

This means that the `manifestoo -d <addons dir> list` and `manifestoo -d
<addons dir> list-depends` work without additional options.

## From the Odoo configuration

With `--addons-path-from-odoo-cfg` option you can provide an Odoo configuration
file where Manifestoo will look for the `options.addons_path` key to extend its
addons search path.

This option can also be set with the `ODOO_RC` environment variable.

## From the `odoo.addons` namespace

Internally, Odoo builds its addons path into the `odoo.addons.__path__`
variable.

Manifestoo tries to read this value using something roughly equivalent to
`python -c "import odoo.addons; print(odoo.addons.__path__)`.

The python interpreter used to this end can be configured using the
`--addons-path-python` options. By default it is the `python` executable found
in `PATH`.

This behaviour can be disabled with `--no-addons-path-from-import-odoo`.

## From a list of directories

With the `--addons-path` option, you can add a comma-separated list of
directories to the addons search path.
