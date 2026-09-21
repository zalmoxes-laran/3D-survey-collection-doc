.. _import-gpr:

Import GPR depth slices (georadar)
==================================

3DSC ingests **ground penetrating radar depth slices** and places them
under the survey area at the depth they were measured at, so that a
buried anomaly can be read in the same space as the photogrammetric
model of the ground above it.

.. seealso::

   :ref:`gpr-slices` documents every field of the panel;
   :ref:`gpr-representation` explains why a slice becomes a textured
   surface, how the drape works, and where the importer deliberately
   stops.

When to use this recipe
-----------------------

Reach for it when you have **processed depth slices** — the 2D
amplitude maps a GPR suite writes out for successive depth bands — in
either of two shapes:

- **One CSV per slice**, a complete regular grid in raster order, with
  the cell size and the depth in the header line. Cells outside the
  surveyed polygon may carry an empty amplitude field; they become
  transparent.
- **One image per slice**, with the depth in the file name
  (``Slice_-2889mm.jpg``, ``slice_1.900 - 2.000m.png``), optionally
  with an ESRI world file for the extent.

Raw radargrams, traces along profiles and vendor-native acquisition
files are **not** handled: they are sparse data along lines, and must
be processed into depth slices first.

Prerequisites
-------------

- The ``.blend`` file is **saved on disk**, so the cache and any
  ``SHIFT.txt`` land in a predictable place.
- You know the **origin of the survey grid** in the project CRS, or a
  world file beside the rasters carries it. CSV grids usually start at
  ``0, 0`` and carry no georeference at all.
- For draping: the **photogrammetric model of the ground surface** is
  in the scene, already positioned in the same shifted frame as the
  rest of the project.

Step 1 — Point 3DSC at the slices
---------------------------------

In the 3D Viewport sidebar (``N``) switch to the *3DSC* tab and expand
**GPR slices**. Use the folder button to select the folder holding the
slices; 3DSC reports how many it found and the depth range they cover.

Set **CSV grids** or **Images** to match your input.

Step 2 — Build the raster cache (CSV only)
------------------------------------------

Choose a **Colormap** and a **Normalise** mode — leave *Whole stack*
unless you specifically want to chase faint deep anomalies — then press
**Build raster cache**.

The conversion writes one PNG per slice plus a ``gpr_stack.json``
manifest. It is modal, so the interface stays alive and ``Esc``
cancels. As an order of magnitude: forty slices of 87 MB each convert
in about half a minute and produce a cache of some 40 MB, against 3.3
GB of source CSV.

.. admonition:: Remember

   This is a one-off. Later imports read the manifest and are
   instantaneous. Keep the cache folder: it is a compact, archivable
   form of the stack, and it is the same shape as a stack that arrives
   already rasterised.

For an **image stack**, press **Read image stack** instead. Nothing is
converted; only the manifest is written. Give the **Cell size** when no
world file sits beside the images.

Step 3 — Georeference and shift
-------------------------------

If a world file was found, the origin is already filled in. Otherwise
type the CRS coordinates of the local ``(0, 0)`` cell into **E** and
**N**, and set **Grid azimuth** if the survey grid is not axis-aligned.

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

3. **Import again.** Each slice now follows the terrain, offset
   downwards by its own depth.

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
once, six hundred of them will occupy several gigabytes.

Step 6 — Record what you read
-----------------------------

When you draw a proxy over an anomaly, select it and press **Tag
selection as read from GPR**. 3DSC writes onto the proxy which slice
documents were on screen, how many, the depth span they cover, and the
acquisition they belong to.

It writes nothing else. Deciding that an amplitude blob is a wall, and
declaring the stratigraphic unit that says so, stays with you — see
:ref:`gpr-representation`.

Troubleshooting
---------------

- **"No gpr_stack.json in …"** — the cache has not been built yet, or
  the Cache field points somewhere else. Build it, or correct the path.
- **The stack lands hundreds of kilometres away** — the origin is
  absolute but the scene shift is zero, or vice versa. Check the
  read-only GSV line under *Apply 3DSC shift*, and remember that 3DSC
  only subtracts the shift from an origin that is genuinely absolute.
- **The stack sits at the scene origin and a warning says so** — the
  dataset is local and no origin was typed. Fill in **E** and **N**.
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
- :ref:`gpr-representation` — the reasoning behind the representation
  and the semantic boundary.
- :ref:`Shifting` and :ref:`shift-coordinates` — the scene-level shift
  this importer consumes.
- :ref:`import-point-data` — sibling recipe, same shift conventions.
