.. _laser-slicer:

.. _LaserSlicer:

Laser Slicer
============

The **Laser Slicer** panel (``OBJECT_PT_Laser_Slicer_Panel``) cuts the
active mesh into a series of cross-sections along a chosen axis and
exports them as SVG files ready for a laser cutter.

This page is the parameter and operator reference for the panel.

Source: ``slicer.py`` (originally by Ryan Southall, integrated into
3DSC). Sidebar tab: *3DSC*. Default state: collapsed
(``DEFAULT_CLOSED``); available only in Object Mode on mesh objects with
faces.

Material dimensions
-------------------

These three values describe the laser-cutter stock and constrain how
slices are laid out on the SVG.

``Thickness (mm)``
   Stock thickness. Drives the slice spacing. Range ``[0.1, 200]``,
   default ``2``.

``Width (mm)``
   Sheet width. Range ``[1, 5000]``, default ``450``.

``Height (mm)``
   Sheet height. Range ``[1, 5000]``, default ``450``.

Cut settings
------------

``DPI``
   Resolution of the laser cutter computer. Range ``[50, 500]``, default
   ``96``.

``Line colour``
   RGB colour of the SVG cut lines. Default red ``(1, 0, 0)``.

``Thickness (pixels)``
   SVG stroke width for cut lines. Range ``[0, 5]``, default ``1``.

``Separate files``
   When enabled, each slice is exported as a separate SVG. When
   disabled, all slices share one SVG.

``Cut position`` (only when ``Separate files = false``)
   How slices are placed on the shared sheet:

   - ``Top left`` — keep the original top-left position;
   - ``Staggered`` — alternated layout;
   - ``Centre`` — recenter every slice.

``Cut spacing (mm)``
   Expected kerf — distance left between adjacent slice outlines.
   Range ``[0, 5]``, default ``1``.

``SVG polygons``
   When enabled, exports each slice as a single closed polygon
   (faster but less accurate). When disabled, exports the actual
   intersection curve (slower, more accurate).

``Export file(s)``
   Destination folder/file path for the SVG output(s).

Slice axis & preview
--------------------

``Slice axis``
   Axis along which the mesh is sliced (``X``, ``Y`` or ``Z``).
   Default ``Z``.

``Show Slice Preview``
   Toggles grease-pencil preview lines in the viewport so you can verify
   the planned cuts before exporting.

The panel also reports the **No. of slices** computed as
``object_height_mm / Thickness`` so you know in advance how many sheets
the job will consume.

Operator
--------

``object.laser_slicer_3dsc`` — *Slice the object*
   Performs the slicing on the active mesh and writes the SVG file(s)
   according to the current settings. The button is enabled only when
   either ``Export file(s)`` is set or the ``.blend`` has been saved.

Typical workflow
----------------

#. Select a watertight mesh.
#. Enter material dimensions (Thickness, Width, Height) for your laser
   cutter stock.
#. Pick a ``Slice axis``.
#. Toggle ``Show Slice Preview`` to verify the cuts.
#. Set ``Export file(s)`` and press *Slice the object*.
