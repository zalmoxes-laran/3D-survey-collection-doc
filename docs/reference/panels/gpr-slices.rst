.. _gpr-slices:

GPR slices
==========

.. seealso::

   This page is the **parameter reference** for the GPR slices panel.
   For the end-to-end recipe see :ref:`import-gpr`; for why a depth
   slice is represented as a textured surface rather than a point
   cloud or a voxel volume, see :ref:`gpr-representation`.

.. _GPRpanelFIG:

.. figure:: /img/GPR_panel.png
   :width: 300
   :align: center

   The GPR slices panel, with a CSV stack cached, georeferenced and
   draped on a declared photogrammetric ground

The panel (:numref:`Fig. %s <GPRpanelFIG>`) ingests **ground penetrating
radar depth slices** — the 2D amplitude maps a GPR processing suite
produces for successive depth bands — and places them in the Blender
scene at their correct depth below a survey area.

It reads two shapes of input. **CSV grids** are one file per slice,
each a complete regular grid in raster order with the cell size and the
slice depth in the header line. **Images** are slices already
rasterised, with the depth encoded in the file name and, optionally, an
ESRI world file for the extent.

.. admonition:: Remember

   The panel handles **processed time slices**, not raw radargrams.
   Traces along profiles and vendor-native acquisition files must be
   processed into depth slices by the geophysicist's own suite first.

Slices and cache
----------------

**Slices**
   Folder holding the depth slices. The folder picker beside the field
   also reports how many slices were found and the depth range they
   cover.

**Cache**
   Where the PNG raster cache and its ``gpr_stack.json`` manifest are
   written. Leave empty to use a ``_3dsc_gpr_cache`` folder beside the
   slices.

**CSV grids / Images**
   Which reader to use. *CSV grids* converts the source into the cached
   PNG stack; *Images* describes an already rasterised stack without
   converting anything. Both produce the same manifest, so everything
   downstream behaves identically.

Raster cache
------------

Only shown for CSV input; image stacks are used as they are.

**Colormap**
   ``Greyscale`` (high amplitude white), ``Greyscale inverted`` (high
   amplitude black) or ``Viridis`` (perceptually uniform).

**Normalise**
   ``Whole stack`` computes one amplitude range for every slice, so
   slices stay comparable with each other. ``Per slice`` stretches each
   slice to its own range, which reveals faint deep anomalies but
   misrepresents relative amplitude — useful for reading, misleading
   for measuring.

**Clip lo % / Clip hi %**
   Robust percentiles used instead of the raw minimum and maximum, so a
   handful of spikes does not flatten the whole stack. Defaults 2 and
   98.

**Max slices**
   Stop after this many slices. ``0`` processes every slice. Useful for
   a quick look at a deep stack before committing to the full
   conversion.

**Build raster cache**
   Runs the conversion. It is modal: the interface stays responsive and
   ``Esc`` cancels. On completion the report gives the slice count and
   the parse time.

.. admonition:: Remember

   The cache is built once. Re-importing reads the manifest and is
   effectively instantaneous, and the cached PNG stack is itself a
   durable, archivable form of the dataset — far smaller than the
   source CSVs.

Georeferencing
--------------

**E / N**
   Coordinates, in the project CRS, of the local ``(0, 0)`` cell of the
   grid. Read automatically from a world file when one sits beside the
   rasters; typed by hand otherwise.

   These two fields are **text**, not numeric sliders, on purpose.
   Blender's float properties are single precision, which quantises a
   six-digit Easting by up to about 3 cm — coarser than the 5 cm cell
   of a typical GPR grid. Holding the origin as text and shifting it
   before it reaches a transform keeps the full precision.

**Grid azimuth**
   Rotation of the survey grid, in degrees counter-clockwise from CRS
   east, for surveys whose grid is not aligned to the axes.

**Round shift to**
   The proposed shift is rounded down to a multiple of this value. A
   round figure is exactly representable as a single-precision float
   and can be retyped into another project by hand.

**Apply 3DSC shift (GSV)**
   Consume the scene's General Shift Value, as every other 3DSC
   importer does. The read-only line below shows the values currently
   held by the scene. See :ref:`Shifting` and :ref:`shift-coordinates`.

.. _GPRdialogFIG:

.. figure:: /img/GPR_shift_dialog.png
   :width: 480
   :align: center

   The shift dialog, raised when the dataset is in absolute coordinates
   and the scene has no shift yet

When the import would place data far from the world origin, the
operator asks before doing so (:numref:`Fig. %s <GPRdialogFIG>`). Four
situations are distinguished:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Situation
     - Behaviour
   * - Absolute coordinates, scene has no shift
     - The dialog reports the origin and the CRS, proposes a rounded
       shift, and lets you edit it before importing.
   * - Scene has a shift, CRS matches
     - Imports directly; the report confirms that the scene shift was
       reused and that both sides agree on the EPSG code.
   * - Scene has a shift, CRS differs
     - The dialog warns. The scene shift is **not** modified unless you
       explicitly ask for it.
   * - Dataset is already local
     - No shift is applied. A warning is issued if the scene carries an
       absolute shift, since the stack will sit at the scene origin
       until an origin is typed.

**Write into the scene shift (GSV)**
   Present in the dialog. When enabled, the accepted values become the
   scene's General Shift Value, so every other 3DSC importer lands on
   the same origin.

Depth reference
---------------

How the slices are placed vertically.

**Flat**
   One horizontal surface per slice. Correct only where the ground is
   level; the *Ground Z* field then gives the absolute elevation of
   depth zero.

**Grid on ground**
   A regular grid over the slice extent, dropped onto the declared
   ground surface by ray casting. *Grid* sets the number of cells per
   side — 128 gives about 16 000 faces and takes a fraction of a
   second.

**Ground geometry**
   A decimated duplicate of the ground mesh itself, for when the
   terrain's own topology matters. *Max triangles* is the budget; the
   count is in triangles because Blender's Decimate modifier works on
   triangles, not quads. The declared ground object is never modified.

**Ground**
   The photogrammetric walking surface the slices hang below. The panel
   warns when the chosen mesh has not been declared as such.

**Declare as photogrammetric ground**
   Marks the active mesh as the walking surface and records its face
   count, so the drape is traceable to the photogrammetric document it
   came from rather than being a silent choice.

.. admonition:: Remember

   Whichever mode is used, the resulting surface is **shared by every
   slice in the stack**. The offset between one slice and the next is a
   pure vertical translation, so forty slices cost one mesh, not forty.
   This is what makes it safe to hang a deep stack under a large
   photogrammetric model.

Stack display
-------------

Shown once a stack has been imported, named after it.

**All / One / Down to**
   Show every slice, only the current one, or everything down to the
   current one. Beyond sixty slices the importer switches to single
   slice display on its own and says so: a deep stack with every slice
   decoded is the one way this feature can exhaust memory.

**Slice**
   The current slice index. Hidden slices have their pixel buffers
   released; Blender re-decodes one in a few milliseconds when it comes
   back.

**Tag selection as read from GPR**
   Records, on the selected proxy objects, which slice documents were on
   screen when the reading was made — see :ref:`gpr-representation` for
   what that means and why the operator stops there.
