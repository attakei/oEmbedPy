========
oEmbedPy
========

.. note::

   This is yet experimental product.
   It will be implemeted needy features incrementaly.

Installation
============

This is uploaded on PyPI.

.. code-block:: console

   pip install oEmbedPy

Usage
=====

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

If you want JSON, use ``--foramt`` option.

.. code-block:: console

   $ oEmbed.py --format=json 'https://www.youtube.com/watch?v=Oyh8nuaLASA'
   {"title":"Yoshi (NES - Nint ..."}

License
=======

Apache License 2.0
