========
oEmbedPy
========

Overview
========

This is `oEmbed <https://oembed.com>`_ client for Python.

Features
========

* Simple usage
* Python 3.x native
* Multiple endpoint discovery

Installation
============

This is uploaded on PyPI.

.. code-block:: console

   pip install oEmbedPy

Usage
=====

Library
-------

.. code-block:: pycon

    >>> from oembedpy.application import Oembed

    >>> oembed = Oembed()
    >>> content = oembed.fetch("https://twitter.com/attakei")
    >>> print(content.type)
    rich

Commandline
-----------

.. note:: It needs Click for using CLI. Run extra install 'cli'.

Simple usage for author's video (omitted some output).

.. code-block:: console

   $ oEmbed.py 'https://www.youtube.com/watch?v=Oyh8nuaLASA'
   title:            Yoshi ( ...
   author_name:      attakei
   thumbnail_height: 360
   thumbnail_width:  400

If you want JSON, use ``--format`` option.

.. code-block:: console

   $ oEmbed.py --format=json 'https://www.youtube.com/watch?v=Oyh8nuaLASA'
   {"title":"Yoshi (NES - Nint ..."}

Others
------

This has extension for easy-using.
Please see `documentation <https://oEmbedPy.rtfd.io>`_.

License
=======

Apache License 2.0
