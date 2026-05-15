.. _import-point-data:

Import points (total station / GPS)
===================================

3DSC ships a **Points as Empty Objects** importer that ingests 2D/3D
point lists exported from total stations, GPS receivers, or any other
surveying device that produces a delimited text file. The importer
honours the project's **geographic shift** values configured at scene
level, so absolute-coordinate point sets land in the same local frame
as the rest of the Blender scene, while purely local datasets can be
imported as-is and georeferenced manually with the recipe at the
bottom of this page.

This page is the canonical tutorial for the **Points as Empty
Objects** button exposed by the *Importers* panel of 3DSC. The short
description of the button in the panel reference (:ref:`Importers`)
covers the UI; the recipe below covers the end-to-end workflow,
including the common case of **mixing total station (local) and GPS
(absolute) survey data** in the same scene.

When to use this recipe
-----------------------

Reach for the point importer when you have:

- A **total station** survey exported as ``.csv`` or ``.txt`` —
  typically a list of named points with X, Y and Z columns expressed
  in a local coordinate frame.
- A **GPS / GNSS** survey exported in the same delimited form, with
  absolute coordinates (UTM or another projected CRS).
- A **mixed dataset** — total station points that must be brought
  into the absolute frame of a GPS survey by means of two or more
  common control points. This is the typical archaeological case
  where a fast local instrument station is later anchored to a few
  GNSS-fixed pegs.

For dense point clouds (laser scanner, photogrammetric sparse cloud)
use the dedicated mesh / point cloud importers instead. The flow on
this page is intended for **discrete, named survey points**.

Prerequisites
-------------

Before launching the importer, make sure that:

- The source file is a ``.csv`` or ``.txt`` with at least **four
  columns** in the order ``name, X, Y, Z`` (extra columns are
  ignored). The column separator can be a comma, a space or a
  semicolon — you will select it in the import dialog.
- A **header row** is acceptable (toggle *Has header* in the dialog).
- For **absolute-coordinate datasets** (GPS, georeferenced total
  station), the scene shift is configured — either by loading a
  ``SHIFT.txt`` file from the :ref:`Shifting` panel, or by setting
  ``scene.BL_x/y/z_shift`` and EPSG manually. See ``3DSC4Metashape``
  for the canonical ``SHIFT.txt`` syntax (``EPSG::NNNN X Y Z``).
- For **purely local datasets** (a total station survey not yet tied
  to a CRS), no shift is required at import time. The shift will
  only be consumed by the GPS file in the georeferencing recipe
  below.
- The Blender file is **saved on disk** before importing. Saving the
  ``.blend`` first keeps related artefacts (``SHIFT.txt`` placed
  alongside, exports written next to the file) consistent.

Basic workflow — Importing points (with SHIFT)
----------------------------------------------

.. TODO: screenshot — Importers panel with the "Points as Empty Objects" button highlighted, plus the file-browser options panel (column mapping, separator, Shift coordinates, Has header)

.. image:: /_static/tutorials/import_points/01_panel.png
   :width: 480
   :align: center
   :alt: 3DSC Importers panel and the Points as Empty Objects dialog

1. **Open the 3DSC Importers panel** — in the Blender 3D Viewport
   sidebar (``N`` key) switch to the *3DSC* tab and expand
   :ref:`Importers`.

2. **Click "Points as Empty Objects"** — a file browser opens.
   Locate the ``.csv`` or ``.txt`` file produced by your total
   station or GPS receiver.

3. **Open the import options** — press the gear icon
   (*Toggle Region*) on the right of the file browser. Map the
   first four columns to ``name`` / ``X`` / ``Y`` / ``Z`` and
   choose the column separator (comma, space, or semicolon) that
   matches your file.

4. **Apply the geographic shift (when applicable)** — enable
   ``Shift coordinates`` if the file holds **absolute** coordinates
   (typical GPS export, or a georeferenced total station survey).
   3DSC will subtract ``scene.BL_x/y/z_shift`` from each row before
   creating the empties, so the points land at viewport-friendly
   values that match the rest of the scene.

   Leave ``Shift coordinates`` **off** if the file holds **local**
   coordinates only — for example a raw total station export that
   you intend to georeference manually later (see the dedicated
   recipe below).

5. **Toggle *Has header*** — enable it when the first row of the
   file is a column header rather than a data point. Leave it off
   when the file starts immediately with values.

6. **Confirm the import** — 3DSC reads the file, creates one empty
   object per row, and groups all empties under a new collection
   named after the source file.

Output
------

After a successful import you will find, in the Blender Outliner:

- A new **collection** named after the source file (without
  extension), grouping every imported point in a single logical
  container. Importing a second file produces a second, separate
  collection — so total station and GPS surveys remain visually
  distinguishable in the Outliner.
- One **empty object per row** of the source file. The empty takes
  the value of the *name* column as its Blender object name; its
  *location* is the row's ``X, Y, Z`` minus the scene shift (when
  ``Shift coordinates`` was on) or the raw ``X, Y, Z`` (when it was
  off).
- No mesh data is created — points are pure empties, which keeps the
  scene light and makes them easy to use as anchors, parent targets
  or photogrammetric control markers.

.. admonition:: Remember

   Use the same convention for **all** absolute-coordinate files in
   one scene: either always consume the shift on import (recommended
   for GPS and georeferenced total station data), or never consume
   it (for a fully local working session). Mixing the two conventions
   inside the same file is the most common source of "points end up
   at the wrong place" tickets.

Recipe: Georeferencing total station points onto GPS points
-----------------------------------------------------------

**Use case.** You have a total station survey expressed in **local
coordinates** (the instrument's own origin and orientation) and a
GPS survey expressed in **absolute coordinates** (UTM or another
projected CRS). At least **two points** were measured by both
instruments — the same physical pegs visible in both datasets. You
want to rigidly transform the total station block onto the GPS
points, without re-running the field acquisition.

**Pre-requisites.** At least two common points between the total
station survey and the GPS survey. The more common points are
available, the easier it is to verify the final alignment by eye,
but two are sufficient when the planimetry is roughly horizontal.

**Step-by-step workflow**

.. TODO: GIF — full georeferencing workflow (parent → cursor-to-selected → selection-to-cursor → rotate → unparent keep)

.. image:: /_static/tutorials/import_points/georef_workflow.gif
   :width: 540
   :align: center
   :alt: End-to-end georeferencing of total station points onto GPS points

1. **Import the GPS file consuming SHIFT.** The GPS dataset is in
   absolute coordinates, so the importer must subtract the scene
   shift to keep the points close to the Blender origin. Use the
   basic workflow above with ``Shift coordinates`` enabled.

2. **Import the total station file without consuming SHIFT.** The
   total station dataset is in local coordinates — a rigid block
   that you will move and rotate as a whole. Use the basic workflow
   above with ``Shift coordinates`` disabled.

3. **Align the total station block to the GPS frame in viewport.**

   a. In the Outliner (or the viewport), select **all total station
      points**, then designate **one of the two common points** as
      the *handle* by Shift-clicking it last so it becomes the
      *active* object. The handle is the pivot around which the
      whole block will rotate.

   b. Press **Ctrl+P** and choose *Set Parent → Object*. Every
      total station empty is now a child of the handle: moving or
      rotating the handle moves and rotates the entire block as a
      rigid unit.

   c. Select the **GPS point** that corresponds to the handle —
      same physical peg, in the GPS collection.

   d. Press **Shift+S** and choose *Cursor to Selected*. The 3D
      cursor jumps to the absolute position of the GPS point.

   e. Select the **total station handle** again, making sure it is
      the active object.

   f. Press **Shift+S** and choose *Selection to Cursor*. The
      handle snaps to the 3D cursor — and, because every other
      total station point is parented to it, the whole block
      translates as one rigid body onto the GPS point.

   g. **Rotate the block.** With the handle still selected (parent
      object), press ``R`` followed by the rotation axis — usually
      ``Z`` when the planimetry is horizontal, because the
      horizontal alignment is the unknown after translation. Rotate
      until the **second common point** of the total station block
      visually overlaps its GPS counterpart. Zoom in for accuracy
      and **hold Shift** during the rotation to enter fine-motion
      mode for sub-degree adjustments.

   h. Confirm the rotation with **Enter**.

4. **Bake the alignment into the children.** Select all total
   station points **plus** the handle, then press **Alt+P** and
   choose *Clear and Keep Transformation*. The parent relationship
   is dissolved, but every child retains the world position and
   rotation it had under the parent. The total station points are
   now standalone empties at their georeferenced locations.

5. **Inspect the result.** The two common points should sit
   essentially on top of their GPS counterparts. Any residual
   discrepancy is the survey error budget — small with well-fixed
   pegs, larger with hand-held GPS measurements. If the two
   alignments look correct but the rest of the block is offset,
   review the rotation axis (see *Troubleshooting* below).

.. TODO: screenshot — final aligned state in the viewport, with the two common points overlapping and the rest of the total station block in place

.. image:: /_static/tutorials/import_points/02_aligned.png
   :width: 480
   :align: center
   :alt: Total station points after alignment, overlapping the GPS control pair

**Export the aligned dataset for photogrammetry**

Once the total station block sits in the absolute frame, you usually
want to push it back out to a photogrammetric package
(Metashape, RealityCapture, etc.) as ground control markers:

- Select **all aligned total station points**.
- Use the *Coordinates* export of the :ref:`Exporters` panel
  (``.csv`` or ``.txt``), enabling ``Add names of objects`` so each
  row keeps its survey label, and ``World shift coordinates`` so the
  scene shift is **added back** on the way out.
- The resulting file holds the original survey names paired with
  absolute coordinates — a drop-in ground control file for any
  photogrammetric suite. See ``3DSC4Metashape`` and
  ``3DSC4RealityCapture`` for the matching import steps on each
  software.

Troubleshooting
---------------

- **All points stack at the world origin (0, 0, 0)** — the file
  holds absolute coordinates but ``Shift coordinates`` was left off
  (or the scene shift is still at zero). Configure the scene shift
  through the :ref:`Shifting` panel, then re-import with the option
  enabled.
- **Points appear scattered millions of metres from the scene
  origin** — the opposite case: the file is already in local
  coordinates, but the import was run with ``Shift coordinates`` on
  while a non-zero scene shift was set. Disable the option and
  re-import.
- **The parent relationship is lost after rotation** — when ending
  the alignment, you must use **Alt+P → Clear and Keep
  Transformation**, *not* the plain *Clear Parent* entry. Plain
  *Clear Parent* snaps the children back to their pre-parenting
  positions and undoes the whole alignment. If this happened, undo
  with ``Ctrl+Z`` and re-apply *Clear and Keep Transformation*.
- **The second common pair does not align after rotation** — you
  probably rotated around the wrong axis. The default
  ``R`` → ``Z`` works only when the survey planimetry is roughly
  horizontal. For tilted survey planes, try ``R`` → ``X`` or
  ``R`` → ``Y`` instead, or rotate freely (``R`` with no axis
  constraint) while watching the second point converge.
- **Points imported with garbled names or wrong coordinates** — the
  column separator or the *Has header* toggle was likely wrong.
  Delete the collection, re-open the importer, and double-check
  the separator and header settings before confirming.

Related recipes
---------------

- :ref:`Importers` — short reference description of every button in
  the Importers panel, including *Points as Empty Objects*.
- :ref:`Shifting` — how to configure the scene-level
  ``BL_x/y/z_shift`` values consumed by this importer.
- :ref:`import-batch-obj` — sibling recipe for photogrammetric model
  ingestion (Batch OBJ), which also honours the scene shift.
- :ref:`import-cad` — sibling recipe for CAD/DXF vector imports.
- ``3DSC4Metashape`` and ``3DSC4RealityCapture`` — the canonical
  consumers of the georeferenced point file exported at the end of
  the recipe above (use the survey points as photogrammetric ground
  control markers).
