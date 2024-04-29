=========
Workspace
=========

oEmbedPy uses user local directory to management configuration and cache.

About workspace
===============

Workspace is construction to manage local state of oEmbed by ``oEmbed.py``.
You can empower performance of oEmbed.py to use workspace instead of simple CLI.

Behaviors of workspace
======================

Cache of provider list
----------------------

oEmbed.py fetch https://oembed.com/providers.json to collect providers' URL.
With workspace, cache fetched json file in 1 day to reduce requests.

Cache of responses from providers
---------------------------------

oEmbed content may have to response with ``cache_age`` parameter.
With workspace, CLI save content with ``cache_age`` into cache and reuse it until expired.

Usage for workspace
===================

In CLI command
--------------

Add ``-w/--workspace`` option with CLI.

In Sphinx extension
-------------------

Set :confval:`oembed_use_workspace` into your ``conf.py``.

Remove caches
-------------

oEmbedPy uses :pypi:`platformdirs` to manage locale of caches.
If you want to remove caches' files, refer to ``user_data_path``.

example:

.. list-table::

   - * macOS
     * ``/Users/{USERNAME}/Library/Application Support/oembedpy``
   - * Windows
     * ``C:\Users\{USERNAME}\AppData\Local\Acme\oembedpy``
   - * Linux
     * ``/home/{USERNAME}/.local/share/oembedpy``
