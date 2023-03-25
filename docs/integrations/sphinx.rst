========================
Work as Sphinx extension
========================

You can embed HTML content from oEmbed API.

Set up
======

.. code-block:: python

   extensions = [
       # After extensions
       "oembedpy.ext.sphinx",
   ]

Usage
=====

Write ``oembed`` directive into your document.

.. code-block:: rst

   .. oembed:: CONTENT-URL

When it build, embed ``iframe`` content into your HTML.

Spec of directive
-----------------

.. rst:directive:: oembed

   .. rst:directive:option:: maxwidth
      :type: int

      Max width for embed content.
      This value is used by API request.

   .. rst:directive:option:: maxheight
      :type: int

      Max height for embed content.
      This value is used by API request.

Example
=======

Simple using
------------

.. code-block:: rst

   .. oembed:: https://www.youtube.com/watch?v=Oyh8nuaLASA

.. oembed:: https://www.youtube.com/watch?v=Oyh8nuaLASA

With options
------------

.. code-block:: rst

   .. oembed:: https://www.youtube.com/watch?v=Oyh8nuaLASA
      :maxwidth: 640
      :maxheight: 640

.. oembed:: https://www.youtube.com/watch?v=Oyh8nuaLASA
   :maxwidth: 640
   :maxheight: 640
