0.4.0 (2022-05-12)
==================

Features
--------

- Add ``list-codepends`` to print the set of addons that depend on the select addons. (`#7 <https://github.com/sbidoul/manifestoo/issues/7>`_)
- Add ``list-missing`` command (`#22 <https://github.com/sbidoul/manifestoo/issues/22>`_)
- As in Odoo, the existence of an ``__init__.py`` file is now asserted to determine valid addons path. (`#25 <https://github.com/sbidoul/manifestoo/issues/25>`_)
- Update Odoo core addon lists. (`#26 <https://github.com/sbidoul/manifestoo/issues/26>`_)


0.3.1 (2021-11-11)
==================

Bugfixes
--------

- Fix core Odoo addons path discovery for Odoo < 13.0. (`#18 <https://github.com/sbidoul/manifestoo/issues/18>`_)

Features
--------

- Update base addons list


0.3 (2021-10-06)
================

Features
--------

- Add support for Odoo 15, and update Odoo base addons lists. (`#15 <https://github.com/sbidoul/manifestoo/issues/15>`_)


Improved Documentation
----------------------

- Document addons selection and search path options. (`#3 <https://github.com/sbidoul/manifestoo/issues/3>`_)


0.2 (2021-05-25)
================

Deprecations and Removals
-------------------------

- Deprecate ``--separator`` as a global option. It belongs to commands that print
  lists. (`#1 <https://github.com/sbidoul/manifestoo/issues/1>`_)


0.1 (2021-05-23)
================

First release.
