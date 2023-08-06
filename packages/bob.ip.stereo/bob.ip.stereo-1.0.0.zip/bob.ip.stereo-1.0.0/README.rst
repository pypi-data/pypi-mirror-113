.. -*- coding: utf-8 -*-

.. image:: https://img.shields.io/badge/docs-v1.0.0-yellow.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.ip.stereo/v1.0.0/index.html
.. image:: https://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.ip.stereo/v1.0.0/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.ip.stereo/badges/v1.0.0/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.stereo/commits/v1.0.0
.. image:: https://gitlab.idiap.ch/bob/bob.ip.stereo/badges/v1.0.0/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.stereo/commits/v1.0.0
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.ip.stereo
.. image:: https://img.shields.io/pypi/v/bob.ip.stereo.svg
   :target: https://pypi.python.org/pypi/bob.ip.stereo


=============
Bob IP Stereo
=============

This package is part of the signal-processing and machine learning toolbox Bob_.

This package implements stereo mapping and projection functionalities and provides 
them as ``bob.io.stream.StreamFilter`` to easiily integrate them in processing 
pipelines.


Installation
------------

Complete bob's `installation`_ instructions. Then, to install this
package, run::

  $ conda install bob.ip.stereo


Example
-------

Here is an example of how to use the package to load data recorded with 3 different cameras, build a depth map using 
2 of them and use it to project the third camera's data.

.. code-block:: python

   # Import Stream and StreamFile classes
   # Generic processing filters are available through the Stream class
   from bob.io.stream import StreamFile, Stream

   # Import bob.ip.stereo: this updates the Stream class with the stereo filters
   # It also upates the StreamFile class to allow to set camera configuration information.

   f = StreamFile(
      resource_path("test/data/input_example.h5", "bob.io.stream"),
      resource_path("config/idiap_face_streams.json", "bob.io.stream"),
   )
   f.set_camera_configs(resource_path("config/idiap_face_calibration.json"))

   # stream for stereo and projection tests
   color = Stream("color", f)
   nir_left = Stream("nir_left_stereo", f).adjust(color)
   nir_right = Stream("nir_right_stereo", f).adjust(color)
   
   # reproject operations
   map_3d = nir_left.stereo(nir_right)
   depth = map_3d.select(channel=2).colormap(colormap="jet")
   rep_color = color.reproject(nir_left, nir_right, map_3d)

   # Use the stereo data:
   rep_color[0:2]  # ...


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
