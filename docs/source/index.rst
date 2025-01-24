Welcome to vfbLib's documentation!
===================================

`vfbLib`` is a converter and deserializer for FontLab Studio 5 VFB files.

FontLab’s own `vfb2ufo` converter is from 2015, only outputs UFO v2, and
contains serious bugs that are never going to be fixed. Its support on macOS is
subject to Apple’s mercy (no native support for Apple Silicon).

That’s why a single determined programmer with a hex editor set out to rectify
this situation.

The VFB file format is described in the
`vfbLib-rust <https://github.com/jenskutilek/vfbLib-rust/blob/main/FILEFORMAT.md>`__ repo,
a work-in-progress implementation of vfbLib in rust.

Check out the :doc:`usage` section for further information, including
how to :ref:`installation` the project.

.. note::

   This project is under active development.

Contents
--------

.. toctree::
   :maxdepth: 2

   usage
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`