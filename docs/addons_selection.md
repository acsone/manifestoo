# Selecting addons

Manifestoo works on lists of addons. The options starting with `--select` are
used to tell it which addons to work on.

```{tip}
The addons selection options below are additive.
```

## Selecting all addons in a directory

`--select-addons-dir` (or `-d` for short) lets you select all addons in a directory.

```{tip}
This option may be repeated to select several directories.
```

```{tip}
Addons that have the `installable` flag set to `False`,
or addons with a missing or invalid manifest are ignored.
```

## Selecting individual addons

With `--select-include` (abbreviated `--select`), you can provide a
comma-separated list of addon names.

```{tip}
This is useful for instance with the `tree` command, so to display the dependency
tree of your great application, use: `manifestoo --select my_great_app tree`.
```

## Selecting Odoo core addons

It is sometimes useful to know the list of core Odoo addons from the community
and enterprise editions. The `--select-core-addons` option lets you do just that.

Manifestoo will try to detect the Odoo version from the version key of addons
found in the addons search path. If it cannot detect it, you can provide it
with `--odoo-series`.

So for example, this will print the list of core Odoo addons for Odoo version 13.0:

```console
manifestoo --select-core-addons --odoo-series=13.0 list
```

```{note}
The list of core Odoo addons is static and part of the manifestoo release.
```

## Selecting found addons

You can use `--select-found` to include all addons that are found in the
[addons search path](addons_path).

## Excluding addons

With `--select-exclude`, you can provide a comma separated list of addons to
exclude from the selection.

Add `--exclude-core-addons` and only non-core addons will be selected.

This can be useful in combination with `--select-addon-dir`.
