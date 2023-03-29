0.7 (2023-02-07)
================

Features
--------

- Add ``--select-found`` flag to select all addons available to the detected Odoo isntallation. (`#17 <https://github.com/acsone/manifestoo/issues/17>`_)
- Add ``--exclude-core-addons`` option. (`#53 <https://github.com/acsone/manifestoo/issues/53>`_)


0.6 (2022-12-11)
================

Features
--------

- Add `-i/--interactive` option to the tree command, to display an interactive tree. (`#161 <https://github.com/acsone/manifestoo/issues/161>`_)


Deprecations and Removals
-------------------------

- Drop Python 3.6 support. (`#161 <https://github.com/acsone/manifestoo/issues/161>`_)


0.5 (2022-09-24)
================

Misc
----

- Relax the typer dependency version constraint. (`#30 <https://github.com/acsone/manifestoo/issues/30>`_)
- Part of `manifestoo` has been extracted to `manifestoo-core`, which will evolve into
  a lightweight library to reason about Odoo addons manifests. (`#32 <https://github.com/acsone/manifestoo/issues/32>`_)


0.4.2 (2022-05-13)
==================

Bugfixes
--------

- Add ``--no-transitive`` and ``--no-include-selected`` options to the ``list-codepends``
  so the default values can be switched off. (`#28 <https://github.com/acsone/manifestoo/issues/28>`_)


0.4.1 (2022-05-12)
==================

- Packaging tweaks, no feature change.
- Add development workflow documentation page.

0.4.0 (2022-05-12)
==================

Features
--------

- Add ``list-codepends`` to print the set of addons that depend on the selected addons. (`#7 <https://github.com/acsone/manifestoo/issues/7>`_)
- Add ``list-missing`` command to print the missing dependencies of the selected addons. (`#22 <https://github.com/acsone/manifestoo/issues/22>`_)
- As in Odoo, the existence of an ``__init__.py`` file is now asserted to determine valid addons path. (`#25 <https://github.com/acsone/manifestoo/issues/25>`_)
- Update Odoo core addon lists. (`#26 <https://github.com/acsone/manifestoo/issues/26>`_)


0.3.1 (2021-11-11)
==================

Bugfixes
--------

- Fix core Odoo addons path discovery for Odoo < 13.0. (`#18 <https://github.com/acsone/manifestoo/issues/18>`_)

Features
--------

- Update base addons list


0.3 (2021-10-06)
================

Features
--------

- Add support for Odoo 15, and update Odoo base addons lists. (`#15 <https://github.com/acsone/manifestoo/issues/15>`_)


Improved Documentation
----------------------

- Document addons selection and search path options. (`#3 <https://github.com/acsone/manifestoo/issues/3>`_)


0.2 (2021-05-25)
================

Deprecations and Removals
-------------------------

- Deprecate ``--separator`` as a global option. It belongs to commands that print
  lists. (`#1 <https://github.com/acsone/manifestoo/issues/1>`_)


0.1 (2021-05-23)
================

First release.
