.. _import-cad:

Importing CAD files (DXF)
=========================

3DSC supports import of CAD vector files in **DXF** format, including
**georeferenced** DXF files exported from desktop GIS or topographic
suites. The DXF importer respects the project's **geographic shift**
values configured at scene level — meaning that an absolute-coordinate
DXF will be correctly anchored to the local Blender origin defined by
3DSC (and, transitively, by the EM Tools Georeferencing panel when both
add-ons are active).

.. seealso::

   For the rationale behind coordinate shifting (why absolute-coordinate
   CAD data needs to be offset on import), see :ref:`shift-coordinates`.

When to use this recipe
-----------------------

Reach for the DXF import flow when you have:

- Topographic surveys (contour lines, breaklines) saved as DXF.
- Architectural restitutions (plans, elevations) shared by colleagues
  in CAD.
- Engineering or cadastral overlays that need to coexist with your
  photogrammetric meshes inside Blender.

For point clouds, photogrammetric meshes or textured assets, use the
dedicated 3DSC importers (e.g. ``Import → 3DSC → Photogrammetric
model``). The DXF flow is intended for **vector** CAD content only.

Dependency: ``ezdxf``
---------------------

The 3DSC DXF importer reads the file with the
`ezdxf <https://ezdxf.readthedocs.io>`_ Python library. If it is not
already in Blender's Python, the importer reports an explicit error
and points you to the DXF Import panel, which exposes a one-click
installer. Install ``ezdxf`` once per Blender major version.

How the geographic shift is applied
-----------------------------------

The DXF importer reads three scene-level scalars set by 3DSC
(``scene.BL_x_shift``, ``scene.BL_y_shift``, ``scene.BL_z_shift``) and
subtracts them from the absolute DXF coordinates of each imported
entity (LINE, CIRCLE, ARC, POLYLINE, HATCH, TEXT) before instantiating
the Blender geometry. The result is that geometries land in the same
local frame as the rest of your scene.

Worked example: if your DXF stores absolute Italian UTM coordinates
(e.g. ``X = 312500.0``) and your scene shift is
``BL_x_shift = 312000.0``, the line will be created at Blender
``X = 500.0`` — comfortable for the viewport and aligned with any
photogrammetric model that was imported with the same shift.

Toggle the shift off (``Shift Coordinates`` checkbox in the import
dialog) when the DXF is already in local coordinates, or for
sanity-check passes. See :ref:`shift-coordinates` for the full
rationale.

Step-by-step workflow
---------------------

1. **Set the scene shift** — either through the 3DSC import of any
   other georeferenced asset, through a ``SHIFT.txt`` file alongside
   your DXF, or by configuring the EM Tools **Georeferencing panel**
   (which writes the same ``BL_x/y/z_shift`` properties).

   See ``3DSC4Metashape`` for the canonical ``SHIFT.txt`` format
   (``EPSG::NNNN X Y Z``).

2. **Open the DXF importer** — ``File → Import → DXF`` (or the
   ``Import DXF`` button in the 3DSC sidebar). The dialog summarises
   the active shift values at the top, under ``Coordinate Settings``.

3. **Choose which entity types to import** — by default LINES,
   CIRCLES, ARCS, POLYLINES, HATCHES and TEXT are all enabled.
   Disable the ones you do not need to keep the scene clean (typical
   archaeological pass: LINES + POLYLINES + TEXT, ignoring hatches).

4. **Optional: merge by layer** — when ``Merge by Layer`` is on,
   line segments belonging to the same CAD layer are stitched into
   polylines using a configurable distance tolerance
   (``Merge Distance Tolerance``, default 0.001 m). This dramatically
   reduces the number of Blender objects when importing dense CAD
   line work.

5. **Run the import** — a new collection is created (named after the
   DXF file) and populated with curve and mesh objects, one per
   merged polyline / circle / arc / hatch / text. The operator
   reports the number of imported entities and the shift that was
   applied.

Coordinate system caveats
-------------------------

- **DXF without embedded CRS** — DXF files do not carry a robust CRS
  declaration. The importer assumes the DXF coordinates are in the
  same CRS as the scene's EPSG. If the source used a different CRS,
  the geometry will appear translated/rotated. Convert the DXF in a
  desktop GIS tool (or in CAD with a proper coordinate transform)
  before import.
- **DXF with a hidden offset** — some CAD workflows apply a "false
  origin" to the DXF coordinates internally (e.g. subtract 7,000,000 m
  from Y to keep CAD precision). The 3DSC importer subtracts the
  *scene* shift, not any internal CAD shift; you may need to compose
  the two manually before import.
- **3DSC and EM Tools share the same shift** — when both add-ons are
  installed, edits in the EM Tools Georeferencing panel propagate to
  ``scene.BL_x/y/z_shift`` automatically, so the DXF importer sees a
  single, coherent reference. If only 3DSC is installed, set the
  shift through the 3DSC properties; the EM Tools panel is not
  required.

The georeferencing values configured for the scene are the **single
source of truth**. If a DXF appears misaligned, audit the DXF's CRS
metadata first, then the scene's shift values — in that order.

Related recipes
---------------

- `EM Tools — Georeferencing panel <https://docs.extendedmatrix.org/projects/EM-tools/en/latest/panels/georeferencing.html>`_
  — sets EPSG and shift, the contract this importer honours.
- ``3DSC4Metashape`` — explains the canonical ``SHIFT.txt`` format and
  how 3DSC reads it on photogrammetric import.
