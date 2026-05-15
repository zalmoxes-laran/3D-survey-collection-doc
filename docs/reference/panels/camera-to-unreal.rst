.. _camera-to-unreal:

.. _CameraToUnreal:

Camera to Unreal
================

The **Camera to Unreal** panel (``VIEW3D_PT_camera_unreal_3dsc``) converts
the transform of the active Blender camera into the coordinate
convention used by Unreal Engine and copies the result to the system
clipboard.

This page is the parameter and operator reference for the panel.

Source: ``camera_unreal_exporter.py``. Sidebar tab: *3DSC*. Default
state: collapsed (``DEFAULT_CLOSED``).

Coordinate conversion
---------------------

Unreal Engine uses a left-handed coordinate system (X forward, Y right,
Z up) measured in centimetres by default, while Blender is right-handed
in metres. The exporter therefore performs:

- axis flip on Y (``v.y → -v.y``);
- unit scaling by ``Scale Factor`` (default ``100``, i.e. metres → cm);
- optional re-centring on the 3DSC SHIFT values when *Use World Shift*
  is enabled.

Parameters
----------

``Scale Factor``
   Unit conversion factor. Default ``100.0`` (metres → centimetres).
   Range ``[0.1, 1000.0]``.

``Use World Shift``
   If enabled, applies ``scene.shift_x / shift_y / shift_z`` to the
   exported translation so the camera lands in the absolute Unreal world
   coordinates rather than the Blender-local ones. Default ``False``.

   The shift values come from the :ref:`Shifting` panel, so configure
   that first when working on georeferenced data.

Operator
--------

``export.camera_to_unreal_3dsc`` — *Export Camera Transform*
   Reads the active camera, applies the conversion and the optional
   shift, and writes the resulting ``Location`` and ``Rotation`` to the
   system console and clipboard in a format ready to paste into Unreal.

UI states
---------

- If the active object is a ``CAMERA``, the panel shows the camera name,
  the export button, and the advanced options box.
- If no camera is selected, the panel shows a warning and a disabled
  *Export* button.

Typical workflow
----------------

#. Configure :ref:`Shifting` if you intend to export in absolute
   coordinates.
#. Select the camera you want to export.
#. Set ``Scale Factor`` (leave at ``100`` for cm output).
#. Tick ``Use World Shift`` if needed.
#. Press *Export Camera Transform*; paste the clipboard content in
   Unreal Engine.
