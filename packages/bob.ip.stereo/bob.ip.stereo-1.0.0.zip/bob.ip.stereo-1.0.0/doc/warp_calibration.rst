.. _bob.ip.stereo.warp_calibration:

----------------
Warp Calibration
----------------

When depth map / 3D pointcloud information is not available, the remapping of streams onto a reference is not useable.
It is however still possible to align images in different streams, by using bounding boxes defined in the reference
stream and applying a linear transform (warp).

This linear calibration is dependent of the distance camera-target: it simply is the shift of a point from on
camera's image to another camera, at a certain distance. Therefore the transform should only be used for images where
the subject is at the same distance from the cameras than during the calibration.

To create such a transform, it is necessary to collect four fixed points, static in all streams. First, capture an hdf5
file with a chessboard target kept static during the whole capture, in front of the camears and at a defined distance.

The calibration can then be performed with the ``warp_calibration.py`` script.


Configuration
-------------

Here is an example of JSON configuration to create for a warp calibration.

.. code-block:: json

    {
        "stream_config" : "/path/to/streams_config.json",
        "pattern_rows": 9,
        "pattern_columns": 6,
        "frame" : 0,
        "streams": {
            "camera1_rgb": null,
            "camera2_thermal":
            {
                "threshold" : 155,
                "closing" : 4,
                "invert" : true
            },
            "camera3_nir":
            {
                "threshold" : 105,
                "closing" : 2,
                "invert" : false
            }
        },
        "duplicate_calibration": {
            "camera3_nir": "camera3_depth"
        }
    }

| - ``stream_config`` : Path to the JSON data config.
| - ``pattern_rows/columns`` : Number of square rows/columns in the chessboard target. See the image below that 
  corresponds to 9x6.
| - ``frame`` : Frame number to select in each dataset in the ``hdf5`` files.
| - ``streams`` : Streams to calibrate. The names must correspond to the stream names in the ``stream_config``.
|   - ``threshold`` : Pixel value (0-255) used to binary threshold grayscale image.
|   - ``closing`` : Closing size in pixel.
|   - ``invert`` : Invert the pixel intensity (used for thermal images, when black square render white pixel under 
  halogen illumination).
| - ``duplicate_calibration`` : To copy the calibration of one streams to another. Used by example for depth stream that
  is aligned with a NIR streams.


calibration
-----------

.. code-block:: sh

    $ warp_calibration.py -i /path/to/capture.h5 -c warp_config.json -vvv -o /path/to/calibration.json

If the chessboard pattern is not automatically found, the image is displayed. The user must click on the internal 4 
side-corners of the chessboard in this order:

1. down-left (in blue)
2. up-left (still in blue)
3. down-right (in yellow)
4. up-right (in yellow)

.. image:: img/warp_calibration_corners.png
   :width: 25 %
   :align: center

If the user does not want to output markers, the window can be closed, the stream will not appear in the JSON output.
