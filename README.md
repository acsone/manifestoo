# manifestoo

Tools to reason about Odoo addons manifests.

```text
Usage: moo [OPTIONS] COMMAND [ARGS]...

  Do things with addons lists.

  Main options of this command select addons on which the subcommands will
  act. Run 'moo <subcommand> --help' for more options.

Options:
  --addons-paths TEXT             [default: ]
  --addons-paths-from-odoo-rc / --no-addons-paths-from-odoo-rc
                                  Expand addons paths by looking into the Odoo
                                  configuration file found at $ODOO_RC, if
                                  present.  [default: False]

  --addons-paths-from-odoo / --no-addons-paths-from-odoo
                                  Expand addons paths by trying to 'import
                                  odoo' and looking at 'odoo.addons.__path__'.
                                  [default: False]

  --include addon1,addon2,...     Comma separated list of addons to include
                                  (default: all installable addons found in
                                  --addons-dir').  [default: ]

  --exclude addon1,addon2,...     Comma separated list of addons to exclude.
                                  [default: ]

  --ignore-missing-dependencies / --no-ignore-missing-dependencies
                                  Do not fail if dependencies are missing.
                                  [default: False]

  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  check-dev-status  Check that addons only depend on addons that have an...
  check-licences    Check that selected addons only depend on addons with...
  list              Print the selected addons.
  list-depends      Print the direct dependencies of selected addons.
  tree              Print a dependency tree of Odoo addons.
```
