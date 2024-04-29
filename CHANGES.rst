===========
Change logs
===========

v0.6.0
======

:date: 2024-04-29 (JST)

Features
--------

* "workspace" to cache responses (optnional)

Fixes
-----

* Reduce requests to providers.json

v0.5.0
======

:date: 2024-04-21 (JST)

Features
--------

* Follow redirects when fetch embed content (`#1 <https://github.com/attakei/oEmbedPy/pull/1>`_)

Others
------

* Use Ruff for formatting and linting

v0.4.0
======

Support easy-using as library

:date: 2023-03-28 (JST)

Features
========

* Support https://oembed.com/providers.json

  * First, find endpoint from JSON.
  * Second, find endpoint from content HTML.

v0.3.2
======

:date: 2023-03-27 (JST)

Fixes
-----

* Fix case that ``content-type`` includes charset
* Display of CLI includes extra parameters

v0.3.1
======

:date: 2023-03-27 (JST)

Bug fix for type behavior

Fixes
-----

* If API response includes un-excepted optionals, Pack ``_extra``

Misc
----

* Change internal code (delegate discovery)
* Add apidoc into documentation

v0.3.0
======

:date: 2023-02-26 (JST)

For Sphinx

Breaking changes
----------------

* CLI options are changed.

  * ``--maxwidth`` to ``--max-width``
  * ``--maxheight`` to ``--max-height``

Features
--------

* Support XML format content.
* Define Sphinx extension.

Fixes
-----

* ``maxheight`` use in API request correctly.

Misc
----

* Manage documentation. See `RTD <http://oembedpy.rtfd.io/>`_
* Add testcases.

v0.2.1
======

:date: 2023-03-24 (JST)

Fixes
-----

* To work when ``--maxwidth`` or ``--maxheight`` do not set.

v0.2.0
======

:date: 2023-03-24 (JST)

Breaking changes
----------------

* Drop ``--json`` option from CLI.
  You can use ``--format=json`` instead of it.

Features
--------

* Add CLI arguments ``--maxwidth`` and ``--maxheight``.
  These are passed to oEmbed API URL as optional parameters.
* Add CLI arguments ``--format``.
  This is used as output format from CLI.


v0.1.1
======

:date: 2023-03-21 (JST)

Misc
----

* Fix installation from README.

v0.1.0
======

:date: 2023-03-21 (JST)

Initial release.

Features
--------

* Implement simple CLI to display oEmbed content.
