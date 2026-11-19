.. _gpr-slices:

Geophysics slices
=================

.. seealso::

   This page is the **parameter reference** for the Geophysics slices
   panel (named *GPR slices* until 1.7.0-dev.66).
   For the end-to-end recipe see :ref:`import-gpr`; for why a depth
   slice is represented as a textured surface rather than a point
   cloud or a voxel volume, see :ref:`gpr-representation`.

.. _GPRpanelFIG:

.. figure:: /img/GPR_panel.png
   :width: 300
   :align: center

   The panel, then named GPR slices, with a CSV stack cached,
   georeferenced and draped on a declared photogrammetric ground

The panel (:numref:`Fig. %s <GPRpanelFIG>`) ingests **geophysical
slices** — the 2D maps a GPR, ERT or magnetic processing suite produces
for successive depth bands, and the vertical sections along its lines —
and places them in the Blender scene at their correct depth below a
survey area.

The reading is done by the core of the geophysics package
(``geofisica_core``), embedded in 3DSC; see :ref:`gpr-core-source`.

.. admonition:: Remember

   The panel handles **processed slices**, not raw radargrams. Traces
   along profiles and vendor-native acquisition files must be processed
   into slices by the geophysicist's own suite first.

Slices and cache
----------------

**Slices**
   Folder holding the depth slices. The folder picker beside the field
   also reports how many slices were found and the depth range they
   cover.

**Cache**
   Where the PNG raster cache and its ``gpr_stack.json`` manifest are
   written. Left empty, *CSV grids* and *Images* use a
   ``_3dsc_gpr_cache`` folder beside the slices, as before; the other
   kinds use the geophysics cache shared with EMStudio,
   ``~/.s3dgraphy/plugins-data/geofisica/cache/<key>/`` (or under
   ``S3DGRAPHY_PLUGINS_DATA_DIR`` when it is set), where the key is the
   digest of the sources and the parameters. The geophysics cache is
   never written inside the folder of the slices.

**Slices are**
   Which reader to use. Every reader produces the same manifest, so
   everything downstream behaves identically.

   .. list-table::
      :header-rows: 1
      :widths: 22 78

      * - Choice
        - What it reads
      * - CSV grids
        - One CSV per depth slice, a complete regular grid with the
          cell size and the depth in the header (CS07 CSIC-Tivoli).
          Converted into the cached PNG stack.
      * - Images
        - Already rasterised slices, depth in the file name, drawn as
          they are; nothing is converted.
      * - GeoTIFF
        - Rasters of values, one band, georeferenced in their tags (UA
          Ilici sectors). Nodata from ``GDAL_NODATA``; cells at 32767
          reported as saturated; a ``.tfw`` beside checked against the
          tags.
      * - ASCII matrices
        - Headerless matrices, ``0`` for no data: slices with the depth
          band in the name (``cm``, ``m`` or ``mm``), sections named
          ``VERT*`` (Basilica Iulia ERT). Extent and section sizes
          declared below.
      * - Points
        - ``X Y Z V`` volumes (one plane per level) or ``line N``
          section files.
      * - Screen captures
        - Captures of the GPR program, placed by their plot frame (UA
          Ilici Alcudia).

**Method**
   *GPR* (ground-penetrating radar), *ERT* (electrical resistivity
   tomography) or *Magnetometry*. It names the identities of the
   documents (``gpr:``, ``ert:``, ``mag:``), the collection of the stack
   (``GPR_…``, ``ERT_…``) and the ramp of *Method's ramp*.

Raster cache
------------

The colour fields are not shown for *Images* and *Screen captures*,
which are used as they are.

**Colormap**
   ``Grayscale`` (high amplitude white), ``Grayscale inverted`` (high
   amplitude black) or ``Viridis`` (perceptually uniform); and the
   ramps of the geophysics package: ``Method's ramp`` (hot for GPR, jet
   for ERT, grey for magnetometry), ``Hot`` (for amplitude), ``Jet``
   (for resistivity), ``Viridis (package)`` and ``Grey (package)``.

**Normalise**
   ``Whole stack`` computes one amplitude range for every slice, so
   slices stay comparable with each other. ``Per slice`` stretches each
   slice to its own range, which reveals faint deep anomalies but
   misrepresents relative amplitude — useful for reading, misleading
   for measuring. ``Fixed range`` uses the **Range** typed below it, in
   the declared unit: the whole colour bar of a report.

**Clip lo % / Clip hi %**
   Robust percentiles used instead of the raw minimum and maximum, so a
   handful of spikes does not flatten the whole stack. Defaults 2 and
   98.

**Quantity / Unit**
   What the values measure, and in which unit. Empty means the method's
   own: amplitude, resistivity, magnetic field. Not shown for *CSV
   grids* and *Images*.

**Declare a value scale**
   For files that hold colour indices, not the quantity — the Basilica
   Iulia's ERT, where 1–255 stand for 0–3500 Ω·m read off the colour bar
   of the report. **From** and **To** are the two ranges (``1, 255`` and
   ``0, 3500``), **Unit** the unit of the second (``ohm.m``), **Source**
   where the scale was read (a figure, a page). The scale is written in
   the manifest and in every stamp as declared, with low confidence,
   never as a measure; the values of the files stay as they are.

**Extent** (*ASCII matrices*)
   Width × height in metres of a matrix slice, when the files do not say
   it (Basilica Iulia: ``92 x 50``). Each file keeps its own grid, so
   cells need not be square.

**Sections** / **Other sections** (*ASCII matrices*)
   Length × depth of each vertical section, ``VERT1=50x8; VERT2=92x9``;
   and the size of a section not in the list.

**Frame X / Frame Y / Frame px** (*Screen captures*)
   The values of the first and last tick on the x axis (Alcudia:
   ``-50, 25``) and on the y axis (``-22, 37``), and the plot box of the
   captures in pixels (left, top, right, bottom). Leave **Frame px**
   empty and it is measured on the first capture by its axes and ticks,
   then written in the field. One frame serves the whole stack.

Numbers are typed with a decimal point; the comma separates values.

**Max slices**
   Stop after this many slices. ``0`` processes every slice. Useful for
   a quick look at a deep stack before committing to the full
   conversion.

**Cell size** (*Images*)
   Pixel size in metres, used when no world file sits beside the images.

**Build raster cache**
   Runs the conversion. For *CSV grids* it is modal: the interface stays
   responsive and ``Esc`` cancels; on completion the report gives the
   slice count and the parse time. For the other kinds a progress bar
   follows the build; the report gives the count, whether the cache was
   built or reused, the time, and the first of the reader's warnings
   (two files with the same values, saturated cells, a ``.tfw`` that
   disagrees with the tags). The folder of the last cache built is shown
   under the button.

**Read image stack** (*Images*)
   Writes only the manifest of an already rasterised stack.

.. admonition:: Remember

   The cache is built once. Re-importing reads the manifest and is
   effectively instantaneous, and the cached PNG stack is itself a
   durable, archivable form of the dataset — far smaller than the
   source CSVs. Every PNG and the manifest carry a stamp beside them,
   ``<file>.stamp.json``: the source files by digest, the parameters,
   and the software (3DSC, then the reading core, each with its version
   and commit).

Georeferencing
--------------

**E / N**
   Coordinates, in the project CRS, of the local ``(0, 0)`` cell of the
   grid. Read automatically from a world file when one sits beside the
   rasters; typed by hand otherwise.

   Read from the tags of a GeoTIFF too.

   These two fields are **text**, not numeric sliders, on purpose.
   Blender's float properties are single precision, which quantises a
   six-digit Easting by up to about 3 cm — coarser than the 5 cm cell
   of a typical GPR grid. Holding the origin as text and shifting it
   before it reaches a transform keeps the full precision.

**EPSG**
   The CRS of the typed origin, for files that say none. Not shown for
   *CSV grids* and *Images*.

**Grid azimuth**
   Rotation of the survey grid, in degrees counter-clockwise from CRS
   east, for surveys whose grid is not aligned to the axes. When it is
   0, the rotation the files declare, if any, is used.

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

Only the slices on the stack's grid are draped. A slice with a grid of
its own is a flat plane of its own, a vertical section an upright plane
along X from the stack's origin, a slice without a depth a plane at
depth zero; the import report counts and names them.

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

Import
------

**Import GPR stack**
   Builds the stack in the scene from its manifest, whatever the method:
   an empty named after the stack, in a collection named by the method,
   and one object per slice or section. Each object carries the identity
   of its document (``em_document_id``: ``gpr:<stack>#d<top>-<bottom>m``
   for a depth band, ``#s<line>`` for a section, ``#<product>`` when the
   depth is not known, with ``ert:`` or ``mag:`` for the other methods),
   its kind (``em_document_kind``: ``gpr_time_slice`` for a GPR slice as
   before, otherwise ``<method>_slice`` or ``<method>_section``), and the
   path of its stamp (``geo_stamp``). Beyond sixty slices the display
   switches to *One*.

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
