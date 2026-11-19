.. _import-gpr:

Import geophysical slices (GPR, ERT, magnetometry)
==================================================

3DSC ingests **geophysical slices** — the depth slices and vertical
sections of a ground penetrating radar (GPR), electrical resistivity
(ERT) or magnetic survey — and places them under the survey area at the
depth they were measured at, so that a buried anomaly can be read in
the same space as the photogrammetric model of the ground above it.

.. seealso::

   :ref:`gpr-slices` documents every field of the panel;
   :ref:`gpr-representation` explains why a slice becomes a textured
   surface, how the drape works, where the reading code lives, and
   where the importer deliberately stops.

When to use this recipe
-----------------------

Reach for it when you have **processed slices**: the 2D maps a
geophysical suite writes out for successive depth bands, or for
vertical sections along a line. The panel reads six shapes of input:

- **CSV grids** — one CSV per slice, a complete regular grid in raster
  order, with the cell size and the depth in the header line (the CS07
  Tivoli stack). Cells outside the surveyed polygon may carry an empty
  amplitude field; they become transparent.
- **Images** — one image per slice, already rasterised, with the depth
  in the file name (``Slice_-2889mm.jpg``,
  ``slice_1.900 - 2.000m.png``), optionally with an ESRI world file for
  the extent. They are drawn as they are.
- **GeoTIFF** — rasters of values, one band, float32, georeferenced in
  their own tags (the sectors of UA Ilici). The nodata value
  (``GDAL_NODATA``) becomes transparent; cells at 32767, the ceiling of
  a 16-bit instrument, are counted and reported as saturated; a ``.tfw``
  beside the file is checked against the tags, and a disagreement of
  half a pixel (centre against corner) is reported.
- **ASCII matrices** — headerless matrices of numbers, one per file,
  ``0`` for no data (the ERT of the Basilica Iulia). Horizontal slices
  carry their depth band in the file name, in centimetres, metres or
  millimetres (``100-150cm.ASC`` is 1.0–1.5 m); files named ``VERT*``
  are vertical sections. The files say nothing of their size: you
  declare the extent of a slice and the length and depth of each
  section.
- **Points** — ``X Y Z V`` volumes, read as one plane for each distinct
  level, or files of ``line N`` blocks, read as sections.
- **Screen captures** — screenshots of the geophysicist's program, one
  per depth, placed by the plot frame of the picture (the 601 captures
  of Alcudia, UA Ilici sector 1). You declare once, for the whole stack,
  which pixels the plot occupies and which metres its first and last
  ticks stand for.

Raw radargrams, traces along profiles and vendor-native acquisition
files are **not** handled: they are sparse data along lines, and must
be processed into slices first.

Prerequisites
-------------

- The ``.blend`` file is **saved on disk**, so the cache and any
  ``SHIFT.txt`` land in a predictable place.
- You know the **origin of the survey grid** in the project CRS, or the
  files carry it (a GeoTIFF's tags, a world file). CSV grids, ASCII
  matrices and screen captures usually start at ``0, 0`` and carry no
  georeference at all.
- For a stack whose files hold **colour indices** rather than the
  measured quantity (the Basilica Iulia's ERT, 1–255 standing for
  0–3500 Ω·m read off the colour bar of the report), the figure the
  scale was read from.
- For draping: the **photogrammetric model of the ground surface** is
  in the scene, already positioned in the same shifted frame as the
  rest of the project.

Step 1 — Point 3DSC at the slices
---------------------------------

In the 3D Viewport sidebar (``N``) switch to the *3DSC* tab and expand
**Geophysics slices**. Use the folder button (**Select slice folder**)
to choose the folder holding the slices; 3DSC reports how many it found
and the depth range they cover.

Choose what the slices are — **CSV grids**, **Images**, **GeoTIFF**,
**ASCII matrices**, **Points** or **Screen captures** — and the
**Method**: **GPR**, **ERT** or **Magnetometry**.

Step 2 — Build the raster cache
-------------------------------

**CSV grids.** Choose a **Colormap** and a **Normalise** mode — leave
*Whole stack* unless you specifically want to chase faint deep
anomalies — then press **Build raster cache**. The conversion writes
one PNG per slice plus a ``gpr_stack.json`` manifest. It is modal, so
the interface stays alive and ``Esc`` cancels. As an order of
magnitude: forty slices of 87 MB each convert in about half a minute
and produce a cache of some 40 MB, against 3.3 GB of source CSV.

**Images.** Press **Read image stack** instead. Nothing is converted;
only the manifest is written. Give the **Cell size** when no world file
sits beside the images.

**GeoTIFF, ASCII matrices, Points, Screen captures.** Fill what the
files do not say, then press **Build raster cache**:

- **Quantity** and **Unit** — what the values measure. Leave them
  empty for the method's own (amplitude, resistivity, magnetic field).
- **Declare a value scale** — when the files hold colour indices, not
  the quantity: **From** ``1, 255``, **To** ``0, 3500``, **Unit**
  ``ohm.m``, and in **Source** the figure or the page it was read from.
  The scale is written as declared, with low confidence, and never
  presented as a measure.
- For **ASCII matrices**: **Extent**, the width × height in metres of a
  horizontal slice (``92 x 50`` for the Basilica Iulia); **Sections**,
  the length × depth of each vertical section
  (``VERT1=50x8; VERT2=92x9``); **Other sections**, the size of a
  section not in the list.
- For **Screen captures**: **Frame X** and **Frame Y**, the values of
  the first and last tick on each axis (Alcudia: ``-50, 25`` and
  ``-22, 37``); **Frame px**, the plot box in pixels (left, top, right,
  bottom). Leave **Frame px** empty and 3DSC measures it on the first
  capture, by its axes and ticks, and writes it in the field for you to
  check.

Type numbers with a decimal point: the comma separates values.

The colour ramps of the geophysics package are offered beside the
classic ones: **Method's ramp** picks hot for GPR, jet for ERT and grey
for magnetometry. **Fixed range** in **Normalise** uses the **Range**
you type, in the declared unit — the whole colour bar of a report, for
instance.

These kinds are cached in the geophysics cache shared with EMStudio
(``~/.s3dgraphy/plugins-data/geofisica/cache/``, one folder per stack,
named by the digest of its sources and parameters), or in the **Cache**
folder you choose — never inside the folder of the slices, which may be
read-only. The same stack read again with the same parameters reuses
its cache. The Basilica Iulia's twelve ERT files are cached in about
half a second.

.. admonition:: Remember

   This is a one-off. Later imports read the manifest and are
   instantaneous. Keep the cache folder: it is a compact, archivable
   form of the stack. Every PNG and every manifest of the cache leaves
   with its stamp beside it (``<file>.stamp.json``): which source files,
   by their digest, it was made from, with which parameters, and by
   which software — 3DSC and the reading core, each with its version
   and commit.

Step 3 — Georeference and shift
-------------------------------

If the files carry their position (a GeoTIFF's tags, a world file), the
origin and the **EPSG** are already filled in. Otherwise type the CRS
coordinates of the local ``(0, 0)`` cell into **E** and **N**, the
**EPSG** of those coordinates, and set **Grid azimuth** if the survey
grid is not axis-aligned. For Alcudia, the origin printed on the
captures is ``701806.741``, ``4234824.081`` in EPSG:25830.

Press **Import GPR stack**.

When the dataset turns out to be in absolute coordinates and the scene
has no shift yet, 3DSC stops and asks
(:numref:`Fig. %s <GPRdialogFIG2>`). The dialog shows where the data
actually is, what the files say about the CRS, and a proposed shift
rounded to a memorable figure. Edit it if you want a different origin,
leave **Write into the scene shift (GSV)** enabled so the rest of the
project lands on the same origin, and confirm.

.. _GPRdialogFIG2:

.. figure:: /img/GPR_shift_dialog.png
   :width: 480
   :align: center

   3DSC asking before placing a dataset that sits hundreds of
   kilometres from the world origin

If the scene already carries a shift, the import goes ahead without
asking — unless the EPSG code of the dataset disagrees with the
scene's, in which case you are warned and the scene shift is left
untouched.

Each slice goes where its manifest puts it:

- a slice on the stack's grid hangs on the stack's shared surface;
- a slice with a grid of its own (each ASCII matrix of the Basilica
  Iulia) gets a flat plane of its own;
- a vertical section stands upright, its length along X from the
  stack's origin and its depth downwards. The files do not say where
  the line of a section runs, and 3DSC says so in a warning: move each
  section onto its line;
- a slice without a depth (a product such as Ilici's ``mean_v2``) lies
  at depth zero, and no depth is written on it.

Step 4 — Hang the slices under the real ground
----------------------------------------------

A slice is a reading taken *below the surface the instrument walked
on*. If that surface is not flat, a flat slice at −1 m is not one metre
below the ground anywhere except by accident.

1. **Select the photogrammetric ground mesh** and press **Declare as
   photogrammetric ground**. 3DSC records the object and its face
   count, so the drape stays traceable to the document it came from.

2. **Choose a depth reference.** *Grid on ground* is the normal choice:
   a regular grid over the slice extent, dropped onto the declared
   surface. Set **Grid** to 128 unless the terrain is unusually broken.
   Use *Ground geometry* only when the terrain's own topology matters —
   a breakline a regular grid would cut across — and set a **Max
   triangles** budget.

3. **Import again.** Each slice on the stack's grid now follows the
   terrain, offset downwards by its own depth. Slices with a grid of
   their own and upright sections stay flat planes; the report counts
   them.

.. _GPRdrapeFIG:

.. figure:: /img/GPR_drape_viewport.png
   :width: 560
   :align: center

   Seven slices of the CS07 Tivoli stack draped on an undulating
   walking surface, sharing one mesh between them

.. admonition:: Remember

   The drape mesh is **shared by the whole stack**, so a deep stack
   under a heavy photogrammetric model costs one surface, not one per
   slice. The declared ground object is never modified: 3DSC always
   works on a copy.

Step 5 — Read the stack
-----------------------

Switch the stack display to **One** or **Down to** and step through the
**Slice** field. Hidden slices release their pixel buffers, so a stack
of several hundred slices stays affordable; with every slice visible at
once, six hundred of them will occupy several gigabytes. Beyond sixty
slices — Alcudia's 601 — 3DSC switches to single-slice display by
itself and says so.

Step 6 — Record what you read
-----------------------------

When you draw a proxy over an anomaly, select it and press **Tag
selection as read from GPR**. 3DSC writes onto the proxy which slice
documents were on screen, how many, the depth span they cover, and the
acquisition they belong to. The button serves every method: the
documents carry their own identity (``gpr:``, ``ert:``, ``mag:``).

It writes nothing else. Deciding that an amplitude blob is a wall, and
declaring the stratigraphic unit that says so, stays with you — see
:ref:`gpr-representation`.

Troubleshooting
---------------

- **"No gpr_stack.json in …"** — the cache has not been built yet, or
  the Cache field points somewhere else. Build it, or correct the path.
- **The cache is refused because it lies under the slices** — the
  geophysics cache never writes beside its sources. Leave **Cache**
  empty, or choose a folder outside the slices.
- **The stack lands hundreds of kilometres away** — the origin is
  absolute but the scene shift is zero, or vice versa. Check the
  read-only GSV line under *Apply 3DSC shift*, and remember that 3DSC
  only subtracts the shift from an origin that is genuinely absolute.
- **The stack sits at the scene origin and a warning says so** — the
  dataset is local and no origin was typed. Fill in **E** and **N**.
- **"The files do not say where the sections run"** — vertical
  sections stand along X from the stack's origin. Move each onto its
  line, as drawn in the geophysicist's report.
- **A warning names two files with the same values** — one of them is
  probably the wrong file (two UA Ilici sectors carry such copies).
  3DSC does not decide which: check with whoever made the data.
- **A GeoTIFF reports saturated cells** — the instrument hit its
  ceiling (32767) there. The cells are drawn; read them with care.
- **"the slice extent does not overlap …"** — the drape found no
  ground under the survey area. The georeferencing origin is wrong, or
  the ground mesh is somewhere else entirely. Fix the origin before
  draping.
- **Part of the drape is flat while the rest follows the terrain** —
  the report counts grid points that missed the ground; those fall back
  to the mean elevation. Extend the ground model, or reduce the slice
  extent.
- **The decimated drape has more faces than the budget** — the budget
  counts **triangles**. A quad mesh has roughly twice as many triangles
  as faces.
- **Blender slows to a crawl on a deep stack** — every visible slice
  decodes its raster. Switch the display to *One*.

Related recipes
---------------

- :ref:`gpr-slices` — every field of the panel.
- :ref:`gpr-representation` — the reasoning behind the representation,
  the one reading core, and the semantic boundary.
- :ref:`Shifting` and :ref:`shift-coordinates` — the scene-level shift
  this importer consumes.
- :ref:`import-point-data` — sibling recipe, same shift conventions.
