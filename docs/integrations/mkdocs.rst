=====================
Work as MkDocs plugin
=====================

You can embed HTML content into MkDocs pages from oEmbed API.

See `demo page <../../demo/mkdocs/>`_.

Set up
======

.. code-block:: yaml

   plugins:
     - oembedpy

Usage
=====

Write TOML format text on code-block fenced ``oembed`` into your document.

.. code-block:: markdown

   ```oembed
   url = 'https://youtu.be/fYzJOI5Ni94'
   ```

When it build, embed ``iframe`` content into your HTML.

Spec of code-block
------------------

* Code fence must be ``oembed``.
* Code body must be formatted as TOML.
* Keys of body are only these:

  * ``url`` (required): Content URL.
  * ``max_width`` (optional): Max width of embed-content.
  * ``max_height`` (optional): Max height of embed-content.

Configuration
-------------

(Not yet)
