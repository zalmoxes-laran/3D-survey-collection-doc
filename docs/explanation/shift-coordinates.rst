.. _shift-coordinates:

==========================================
Coordinate shifting in 3DSC
==========================================

3DSC ships with a **coordinate shifting** mechanism — a scene-level
``BL_x/y/z_shift`` triplet, optionally fed by a ``SHIFT.txt`` sidecar
file — that every 3DSC importer and exporter consults when ingesting or
emitting georeferenced data. This page explains *why* the mechanism
exists, *when* it should be enabled, and *when* it should be left off.
It is the single source of truth that the operational pages
(importers, exporters, photogrammetry recipes, panel reference) link
back to.

.. contents:: On this page
   :local:
   :depth: 2

The problem
===========

Modern survey data is almost always **georeferenced**: total stations,
GPS receivers, photogrammetric pipelines and CAD/GIS suites produce
points and meshes whose coordinates lie hundreds of kilometres from
the projected-CRS origin. A typical UTM Easting can be of order
``500 000 m``; a typical Italian Gauss-Boaga Northing of order
``5 000 000 m``.

Blender, however, stores **vertex coordinates as 32-bit single-precision
floating-point numbers**. Single-precision floats only carry about
**7 significant decimal digits**. As soon as a vertex sits more than a
few kilometres from the world origin, the digits available to encode
millimetre-level geometric detail run out — the result is visible
*jitter*, *shimmering surfaces during navigation*, broken Boolean and
snapping operations, and inaccurate measurements. The further from the
origin, the worse the loss.

This is not a Blender bug — it is a fundamental property of the IEEE-754
single-precision format. Any 3D application built on single-precision
geometry has the same constraint.

The solution
============

3DSC sidesteps the precision problem with a **scene-level coordinate
shift**: an integer-valued (X, Y, Z) offset, expressed in the same CRS
as the source data, that is **subtracted on the way in** and
**added back on the way out**.

Concretely, 3DSC stores three scalars on the Blender scene:

- ``scene.BL_x_shift`` — Easting offset
- ``scene.BL_y_shift`` — Northing offset
- ``scene.BL_z_shift`` — Elevation offset

…plus the EPSG code of the CRS those offsets refer to. The
``SHIFT.txt`` file is simply a one-line text serialisation of the
same four values:

.. code-block:: text

   EPSG::3004 2392800.00 5069900.00 0

When 3DSC imports a georeferenced asset with ``Shift coordinates``
enabled, it subtracts ``(BL_x_shift, BL_y_shift, BL_z_shift)`` from
every vertex / point / DXF entity before instantiating the Blender
object. Geometry that originally sat at ``X = 2 392 950`` lands at
``X = 150`` — well within the safe single-precision range — while
3DSC remembers the offset on the scene.

When 3DSC exports the same asset, the shift is **added back** so the
output file again carries the original absolute coordinates and can
round-trip cleanly into Metashape, RealityCapture, QGIS, ArcGIS, or
any other downstream tool.

When to use it
==============

Enable coordinate shifting whenever you are working with **absolute
coordinates** more than ~1 km from the chosen CRS origin. Concretely:

- Photogrammetric models in **UTM** or any other national projected
  CRS (typical Easting/Northing values in the 100 000–10 000 000 m
  range).
- **GPS / GNSS** survey points in projected CRS.
- **Georeferenced total station** surveys already tied to a CRS.
- **DXF/CAD** drawings exported from desktop GIS or topographic suites
  with absolute coordinates.
- Any asset that must coexist in the same Blender scene with the
  above.

The recommended workflow is to set the shift **once** at the start of
the project — typically by placing a ``SHIFT.txt`` next to the
``.blend`` and loading it through the :ref:`Shifting` panel — and to
keep ``Shift coordinates`` enabled on every subsequent import of
absolute-coordinate data.

When NOT to use it
==================

Leave ``Shift coordinates`` **off** when:

- The source file already holds **local coordinates** (e.g. a raw
  total-station export with the instrument as origin, an architectural
  model in metres from a chosen corner, a photogrammetric chunk
  exported with a *Local* CRS).
- You are running a **sanity-check pass** to verify whether the
  source file is local or absolute.
- The asset is a small object intended to live near the Blender
  origin regardless of the scene shift.

Mixing the two conventions inside the same scene is the most common
source of "objects end up at the wrong place" tickets — see the
operational pages for the specific symptoms and fixes.

Implementation notes
====================

- **Single source of truth** — the scene-level
  ``BL_x/y/z_shift`` scalars and the EPSG code are the canonical
  state. The :ref:`Shifting` panel reads and writes them directly;
  the ``SHIFT.txt`` file is only a bootstrap / portability format.
- **Sidecar location** — ``SHIFT.txt`` is auto-detected when placed
  next to the ``.blend`` file (for the scene-level shift) or
  alongside the ``.obj``/``.dxf``/point files being imported (for
  per-import overrides). The canonical syntax (``EPSG::NNNN X Y Z``,
  space-separated, one line) is shared with the
  :doc:`/reference/tools/metashape-tool` and
  :doc:`/reference/tools/realitycapture-tool` script packages.
- **Interoperability with BlenderGIS** — the :ref:`Shifting` panel
  exposes ``3DSC→GIS`` / ``GIS→3DSC`` buttons to keep the two shifts
  synchronised. Always save the ``.blend`` with a single, coherent
  shift across the two add-ons.
- **Interoperability with EM Tools** — when both add-ons are
  installed, edits in the EM Tools Georeferencing panel propagate to
  ``scene.BL_x/y/z_shift`` automatically, so 3DSC importers see a
  single, coherent reference.
- **``LOCAL`` keyword** — the photogrammetry script packages accept a
  ``LOCAL X Y Z`` form as an alternative to ``EPSG::NNNN X Y Z``,
  which applies the translation without binding to a CRS. Use it
  when the source data is local but you still want to push it
  through the shifted pipeline.

See also
========

Operational pages that implement coordinate shifting in practice:

- :ref:`Shifting` — the panel that reads, writes and synchronises
  the scene-level shift values.
- :ref:`Importers` — short reference of every 3DSC importer button.
- :ref:`import-point-data` — point import recipe (total station /
  GPS), with a worked example of mixing local and absolute datasets.
- :ref:`import-batch-obj` — photogrammetric model import recipe.
- :ref:`import-cad` — CAD/DXF import recipe.
- :ref:`prepare-survey-metashape` — Metashape preparation workflow,
  including the canonical ``SHIFT.txt`` format used by 3DSC for
  Metashape.
- :doc:`/reference/tools/metashape-tool` — full parameter catalogue
  for the Metashape-side scripts that emit and consume ``SHIFT.txt``.
