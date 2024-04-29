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


.. oembed:: https://mastodon.cloud/@attakei/109368512525772407

Usage
=====

Write ``oembed`` directive into your document.

.. code-block:: rst

   .. oembed:: CONTENT-URL

When it build, embed ``iframe`` content into your HTML.

Configuration
-------------

.. confval:: oembed_use_workspace

   :Type: ``bool``
   :Default: ``False``

   Switch to toggle using simple client and workspace.

   If it is set ``True```, extension uses ``Workspace`` object as client.

   .. note:: See :doc:`../workspace` for more information.


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

Gallery
=======

Bluesky
-------

.. code-block:: rst

   .. oembed:: https://bsky.app/profile/attakei.dev/post/3kqigze6cks2z

.. oembed:: https://bsky.app/profile/attakei.dev/post/3kqigze6cks2z

