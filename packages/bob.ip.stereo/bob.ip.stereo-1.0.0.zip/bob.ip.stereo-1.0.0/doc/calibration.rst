.. _bob.ip.stereo.calibration:

------------------
Camera Calibration
------------------

Camera calibration consists in estimating the parameters of a camera, using a set of images of a pattern from the 
camera. The calibration procedure implemented in ``calibration.py`` uses capture files containing synchronous images of 
several cameras to first estimate the intrinsic, then the extrinsic, parameters of the cameras. The script mostly wraps
opencv's algorithms to use with ``bob.io.stream`` data files, therefore it is higly recommended to read opencv's
documentation before using this script.


Camera Parameters
-----------------

The intrinsic parameters of a camera are the paramters that do not depend on the camera's environment. There are composed
of the camera matrix - which describes the transformation between a 3D point in the world coordinate system, to a 2D 
pixel in an image plane, assuming a distortion free projection - and the distortion coefficients of a camera. Opencv's 
camera and distortion model is explained `here
<https://docs.opencv.org/4.5.0/d9/d0c/group__calib3d.html#details>`_.

The extrinsic paramters are the rotation and translation of the camera representing the change of referential from the 
world coordinate to the camera coordinate system. Usually, the position and orientation of one camera, the reference, is
used as the world coordinate system. In that case, the extrinsic parameters of the other cameras encode the relative 
position and rotation of these camera with respect to the reference, which allows to use stereo processing.


Intrinsic Parameters Estimation
-------------------------------

To estimate the intrinsic parameters of a camera, an image of a pattern is captured. The pattern contains points which 
position and distance with respect to each other is known. The first type of patterns to be used were the checkerboard
patterns: the points of interest of the patterns are the inner corners of the checkerboard. The points are alligned, and
the distance between the points is given by the length of a checkerboard square. However, in an image of the pattern, 
the checkerboard corners are not aligned due to distortion, which allows to estimate the distortion coefficients
of the camera's lense. The number of pixels between corners maps to the distance in the real world (square length) and 
allows to estimate the camera matrix.

Opencv's implements methods to detect checkerboard corners, which give precise measurements of the corners in the
image, as is required for intrinsic parameters estimation. However these methods are not robust to occlusion: if a part
of the pattern is hidden, the detection fails. To circumvent this problem, a Charuco pattern can be used: the Charuco
pattern has unique (for a given pattern size) Aruco symbols placed in its white squares. The symbols allow to 
individually identify each corner, so the detection can work even when not all corners are visible.

See opencv's documentation for more explanations on Charuco patterns and how to generate them:
`Detection of ArUco Markers
<https://docs.opencv.org/3.4/df/d4a/tutorial_charuco_detection.html>`_, 
`Detection of ChArUco Corners
<https://docs.opencv.org/3.4/df/d4a/tutorial_charuco_detection.html>`_,
`Calibration with ArUco and ChArUco
<https://docs.opencv.org/4.5.2/da/d13/tutorial_aruco_calibration.html>`_.


Extrinsic Parameters Estimation
-------------------------------

Once the intrinsic parameters of a cameras are known, we are able to "rectify" the camera's image, that is to correct 
the distortion and align the images. When this is done, we can tackle the problem of finding the 
position of the camera with respect to the real world coordinate system. Indeed, the mapping between a 3D point in the 
real world and the corresponding 2D point in the camra's pixels is the projection parametrized by the camera's pose. 
Given enough pair of (3D, 2D) points, the projection parameters can be estimated: this is the so-called 
Perspective-n-Point (PnP) problem.
`Opencv's PnP solver documentation
<https://docs.opencv.org/4.5.0/d9/d0c/group__calib3d.html#ga549c2075fac14829ff4a58bc931c033d>`_.

.. note::
    
    The PnP algorithm works with a set of points which coordinates are known in the coordinate system of the camera's
    images (pixel position in the image) and in the world coordinate system. The world coordinate system origin and 
    orientation can be arbitrary chosen, the result of the PnP will be the camera Pose with respect to that choice. The 
    simplest choice is to place the coordinate system along the checkerboard axis: that way the 3rd coordinate of the 
    corners are (``square_number_along_X`` * ``square_length``, ``square_number_along_Y`` * ``square_length``, 0).

    A minimum of 4 points is needed for the PnP algorithm, however more points helps improve the precision and 
    robustness to outliers.


However, we are not so much interested in knowning 1 camera's pose, rather than to know the position of one camera with
respect to another. In opencv, this is performed by the `stereo calibrate
<https://docs.opencv.org/4.5.0/d9/d0c/group__calib3d.html#ga91018d80e2a93ade37539f01e6f07de5>`_ function, which 
performs the following steps:

* Receive a list of images for each camera, of the same pattern positions (for instance, the images were taken 
  simultaneously with both cameras looking at the pattern).
* For each pair of image from camera 1, camera 2, solve the PnP problem for each camera. Then from the pose of the 2 
  camera with respect to the pattern, compute the pose of one camera with respect to the other.
* Average of the pose obtained for each image pair in previous step.
* Fine tune the pose by optimizing the reprojection error of all points in both cameras. (Levenberg–Marquardt optimizer)
  

.. Note::
    
    The ``stereoCalibrate`` is also able to optimize the intrinsic parameters of the cameras. However, as the number of 
    parameters to optimize becomes big, the results may not be satisfactory. It is often preferable to first find the 
    intrinsic parameters of each camera, then fix them and optimize the extrinsic parameters.


.. image:: img/stereo_diagram.png



``calibration.py``
------------------

The calibration script performs the following steps: 

* Find all the capture files in the input folder. The capture files are ``hdf5`` files containing a dataset per camera,
  and one or more frames per dataset. If specified in the config, only 1 frame will be loaded.
* For each frames for each camera, run the detection to find the pattern points.
* For each camera, using the frames where the pattern could be detected in the previous step, estimate the camera's 
  intrinsic parameters.
* Finaly, the extrinsic parameters of all cameras with respect to a reference (passed as argument) are computed, using
  the frames where enough pattern points for both cameras were detected in the second step. The poses of the cameras are
  then displayed, and the calibration results are written to a ``json`` file.


The calibration script can be called with:

.. code-block:: bash

    $ python calibration.py -c calibration_config.json -r ref_camera -o output.json -v
      usage: calibration.py [-h] [-c CONFIG] [-i INTRINSICS_ONLY] -r REFERENCE
                          [-o OUTPUT_FILE] [-v]

      Calibration script computing intrinsic and extrinsic parameters of cameras
      from capture files. This script performs the following steps: 1. For all
      capture files specified in the configuration json, detect the pattern points
      (first on the image, if failed processes the image (grey-closing,
      thresholding) and tries again) 2. Using the frames were the pattern points
      were detected in step 1: estimate the intrinsic parameters for each stream
      (camera) in the capture files. 3. Againg using the pattern points detected in
      step 1, the extrinsic parameters of the cameras are estimated with respect to
      the reference. 4. The camera poses are displayed, and the results are saved to
      a json file.

      optional arguments:
        -h, --help            show this help message and exit
        -c CONFIG, --config CONFIG
                              An absolute path to the JSON file containing the
                              calibration configuration.
        -i INTRINSICS_ONLY, --intrinsics-only INTRINSICS_ONLY
                              Compute intrinsics only.
        -r REFERENCE, --reference REFERENCE
                              Stream name in the data files of camera to use as
                              reference.
        -o OUTPUT_FILE, --output_file OUTPUT_FILE
                              Output calibration JSON file.
        -v, --verbosity       Output verbosity: -v output calibration result, -vv
                              output the dataframe, -vvv plots the target detection.

An example of a calibration configuration file is given bellow. The ``-r`` switch is used to specify the camera to uses
as the reference for extrinsic parameters estimation. The ``-v`` switch controls the verbosity of the script: setting
``-vvv`` will for instance display the detected patterns points in each frame, to help debugging. 


Calibration configuration example:

.. code-block:: json

    {
        "capture_directory" : "/path/to/capture/folder/",
        "stream_config" : "/path/to/data/streams/config.json",
        "pattern_type": "charuco",
        "pattern_rows": 10,
        "pattern_columns": 7,
        "square_size" : 25,
        "marker_size" : 10.5,
        "threshold" : 151,
        "closing_size" : 2,
        "intrinsics":
        {
            "fix_center_point" : false,
            "fix_aspect_ratio" : false,
            "fix_focal_length" : false,
            "zero_tang_dist" : false,
            "use_intrinsic_guess" : false,
            "intrinsics_guess" :
            {
                "f" : [1200, 1200],
                "center_point" : [540.5, 768],
                "dist_coefs" : [0 ,0, 0, 0, 0]
            }
        },
        "frames_list": {
            "file_1.h5" : [0],
            "file_2.h5" : [2],
        },
        "display":
        {
            "axe_x" : [-60, 60],
            "axe_y" : [-60, 60],
            "axe_z" : [-60, 60]
        }
    }

| - ``capture_directory`` : Path to the folder containing the capture files.
| - ``stream_config`` : Path to the configuration files describing the streams in the capture files. (stream 
  configuration files from ``bob.io.stream``)
| - ``pattern_type`` : Type of pattern to detect in the captures. Only ``chessboard`` and ``charuco`` are currently 
  supported.
| - ``pattern_rows`` : Number of squares in the Y axis in the target.
| - ``pattern_columns`` : Number of squares in the X axis in the target.
| - ``square_size`` : Length of a square in the pattern. This is used as a scale for the real world distances, for 
  instance the distance between the cameras in the extrinsic parameters will have the same unit as the square size.
| - ``marker_size`` : Size of a marker in a charuco pattern.
| - ``threshold`` : Threshold to use for image processing (Adaptative Thresholding) to help with the pattern detection.
| - ``closing_size`` : Size of the grey closing for image processing to help with the pattern detection.
| - ``intrinsics`` : Regroups the parameters of the algorithm used for intrinsic parameters estimation, that is the 
  parameters of opencv\'s ``calibrateCameraCharuco`` or ``calibrateCamera`` functions.
| - ``fix_center_point`` : The principal point is not changed during the global optimization. It stays at the center or 
  at the location specified in the intrinsic guess if the guess is used.
| - ``fix_aspect_ratio`` : The functions consider only fy as a free parameter. The ratio fx/fy stays the same as in the
  input cameraMatrix. (fx, fy: focal lengths in the camera matrix).
| - ``fix_focal_length`` : Fix fx and fy (focal lengths in camera matrix).
| - ``zero_tang_dist`` : Tangential distortion coefficients are fixed to 0.
| - ``use_intrinsic_guess`` : Use the ``intrinsic_guess`` as a starting point for the algorithm.
| - ``intrinsics_guess`` : Starting point for the intrinsic paramters values.
| - ``frames_list`` : Dictionary which keys are the capture files, and values are a list of frames to use in this file.
  **Only the files listed here will be used for the calibration.**
| - ``display`` : Axis limits when displaying the camera poses.


=================
 Calibration API
=================

.. automodule:: bob.ip.stereo.calibration