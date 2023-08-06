.. -*- coding: utf-8 -*-

.. image:: https://img.shields.io/badge/docs-v1.0.0-yellow.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.io.stream/v1.0.0/index.html
.. image:: https://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.io.stream/v1.0.0/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.io.stream/badges/v1.0.0/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.io.stream/commits/v1.0.0
.. image:: https://gitlab.idiap.ch/bob/bob.io.stream/badges/v1.0.0/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.io.stream/commits/v1.0.0
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.io.stream
.. image:: https://img.shields.io/pypi/v/bob.io.stream.svg
   :target: https://pypi.python.org/pypi/bob.io.stream


===============
 Bob IO Stream 
===============

This package is part of the signal-processing and machine learning toolbox Bob_.

Motivation
----------

This package provides a way to define efficient processing pipelines, based on the concept of "streams", to load and 
process or save video data stored in hdf5 files. The stream abstraction allows to define pipelines of processing steps 
with an easy syntax, and provides a way to access the processed data with a "numpy-like" api. It was designed to 
minimize computation and disk access by loading only necessary data and buffering video frames and processed data.

Installation
------------

Complete bob's `installation`_ instructions. Then, to install this
package, run::

  $ conda install bob.io.stream

Example
-------
Here is an example of how to use the package to load data recorded with 3 different cameras, build a processing
pipeline and finally load the data.

.. code-block:: python

   # Import Stream and StreamFile classes
   # Processing filters are available through the Stream class
   from bob.io.stream import StreamFile, Stream

   # Open a Streamfile to a hdf5 file containing video data.
   f = StreamFile("input_example.h5", face_streams.json")

   # Define processing pipeline by chaining streams:
   # First define the streams to load the data from the file (color, left and right), and add some processing
   color = Stream("color", f)
   nir_left = Stream("nir_left_stereo", f).adjust(color).normalize()
   nir_right = Stream("nir_right_stereo", f).adjust(color).normalize()
   all_swir = nir_left.stack(nir_right)

   # Now that the pipeline is defined, the processed data can be accessed as if indexing in a numpy array:
   all_streams[0]  # Loads data and apply processing to provide the first frame of the reprojected stream.
   all_streams[2:10] # Loads several frames, etc...


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _idiap: http://www.idiap.ch
.. _bob: http://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
