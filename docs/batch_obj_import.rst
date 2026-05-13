.. _import-batch-obj:

Importing photogrammetric models (Batch OBJ)
============================================

3DSC ships a **Batch OBJ Import** command that brings several Wavefront
``.obj`` models into Blender in a single pass, preserving the original
alignment, scale and (optionally) the geographic shift stored at scene
level. Use this recipe when an archaeological or architectural dataset
is delivered as a set of tiles or as a series of textured objects that
must coexist in the same Blender scene.

This page is the canonical tutorial for the **Batch OBJ Import**
button exposed by the *Importers* panel of 3DSC. The short description
of the button in the panel reference (:ref:`Importers`) covers the UI;
the recipe below covers the end-to-end workflow.

When to use this recipe
-----------------------

Reach for the Batch OBJ flow when you have:

- A photogrammetric model split into **multiple tiles** exported from
  Metashape, RealityCapture, or any other photogrammetric suite.
- A set of **distinct textured objects** (e.g. individual finds, blocks
  of a wall, stratigraphic units processed separately) that belong to
  the same site and must share a coordinate frame.
- A folder of legacy ``.obj`` exports you need to round-trip through
  Blender, keeping consistent naming and grouping.

For a single ``.obj`` file the standard Blender importer
(``File → Import → Wavefront (.obj)``) is usually enough; the Batch
OBJ Import flow is optimised for **folder-level** ingestion.

Prerequisites
-------------

Before launching the importer, make sure that:

- The source folder contains the ``.obj`` files **plus their
  companion** ``.mtl`` **files and the referenced texture images**
  (typically ``.png`` or ``.jpg``). The ``.mtl`` files are read by
  Blender to recreate the material slots; missing textures will not
  break the import but will yield untextured materials.
- All models share a **common reference frame**. Mixed local /
  georeferenced models in the same batch will land at incompatible
  positions in the Blender viewport.
- If the models are in **absolute (UTM or other projected)
  coordinates**, a ``SHIFT.txt`` file is available — either inside the
  source folder or already loaded into the scene through the
  :ref:`Shifting` panel. See ``3DSC4Metashape`` for the canonical
  ``SHIFT.txt`` syntax (``EPSG::NNNN X Y Z``).
- The Blender file is **saved on disk** before the import. Saving the
  ``.blend`` first lets Blender resolve relative texture paths
  reliably.

Step-by-step workflow
---------------------

.. TODO: screenshot — Importers panel with the Batch OBJ Import (Multiple objs) button highlighted

.. image:: _static/tutorials/batch_obj/01_panel.png
   :width: 480
   :align: center
   :alt: 3DSC Importers panel with the Batch OBJ Import button

1. **Open the 3DSC Importers panel** — in the Blender 3D Viewport
   sidebar (``N`` key) switch to the *3DSC* tab and expand
   :ref:`Importers`.

2. **Click "Batch OBJ Import"** — the button is labelled *Multiple
   objs* in the panel. A file browser opens, anchored to the last used
   location.

.. TODO: screenshot — File browser opened on a sample tiles/ folder, with the right-side options panel expanded

.. image:: _static/tutorials/batch_obj/02_filebrowser.png
   :width: 480
   :align: center
   :alt: Blender file browser with the Batch OBJ Import options panel expanded

3. **Navigate to the source folder** — open the folder that contains
   the ``.obj`` files and their ``.mtl`` / texture companions. You do
   not need to multi-select the files: the operator scans the active
   folder and imports every ``.obj`` found at its top level.

4. **Review the import options on the right side** of the file
   browser. The defaults work for most photogrammetric exports
   (``Z Up`` / ``Y Forward``). If your source pipeline uses a
   different axis convention, set the matching values from the
   drop-down menus before confirming.

5. **Apply the geographic shift (when applicable)** — if the models
   are georeferenced, enable the ``Shift coordinates`` option so that
   3DSC subtracts ``scene.BL_x/y/z_shift`` from the model vertices on
   the way in. The shift values come from the :ref:`Shifting` panel
   or from a ``SHIFT.txt`` file placed alongside the ``.obj`` files.
   Leave the option off for purely local-coordinate datasets.

.. TODO: screenshot — Right-side options panel highlighting Shift coordinates checkbox and axis dropdowns

.. image:: _static/tutorials/batch_obj/03_options.png
   :width: 480
   :align: center
   :alt: Batch OBJ Import options — shift checkbox and axis settings

6. **Confirm the import** — click *Import OBJs* (the confirm button at
   the bottom-right of the file browser). 3DSC iterates over the
   folder and ingests each ``.obj`` as a separate Blender mesh.

Output
------

After a successful import you will find, in the Blender Outliner:

- A new **collection** named after the source folder, grouping every
  imported mesh in a single logical container.
- One **mesh object per source** ``.obj`` **file**, each retaining the
  base name of the source file. Material slots are populated from the
  matching ``.mtl``.
- An optional **empty object** acting as the group anchor when shift
  values have been applied, so the entire batch can be translated or
  parented as a unit without losing relative alignment.

.. TODO: screenshot — Blender Outliner showing the new collection populated with imported meshes

.. image:: _static/tutorials/batch_obj/04_outliner.png
   :width: 480
   :align: center
   :alt: Blender Outliner after a Batch OBJ Import, showing the new collection

.. admonition:: Remember

   By default 3DSC sets imported meshes to *Bounds* display mode for
   performance. Switch to *Textured* in the Object → Viewport Display
   panel to see the photogrammetric materials.

Troubleshooting
---------------

- **Models stack at the world origin (0, 0, 0)** — the ``Shift
  coordinates`` option was probably left off while the source ``.obj``
  files store absolute UTM coordinates. Either re-run the import with
  the option enabled, or set the scene shift through the
  :ref:`Shifting` panel and re-import.
- **Models appear scattered far from the scene origin** — the opposite
  case: shift was applied, but the source files are already in local
  coordinates. Disable ``Shift coordinates`` and re-import.
- **Materials are loaded but textures are missing or pink/magenta** —
  Blender could not resolve the texture paths declared in the
  ``.mtl``. Confirm that the texture files sit in the same folder as
  the ``.obj`` (or that the ``.mtl`` uses relative paths). Saving the
  ``.blend`` before importing helps Blender resolve relative paths
  consistently.
- **Some** ``.obj`` **files are skipped** — only files at the *top
  level* of the source folder are picked up. Move nested ``.obj``
  files up one level, or run the import once per subfolder.
- **Axes look swapped (model lying on its side)** — change the
  ``Forward`` / ``Up`` axis settings in the file-browser sidebar and
  re-import; the defaults match Blender's convention, not every
  photogrammetric exporter.

Related recipes
---------------

- :ref:`Importers` — short reference description of every button in
  the Importers panel.
- :ref:`Shifting` — how to configure the scene-level
  ``BL_x/y/z_shift`` values consumed by this importer.
- :ref:`import-cad` — sibling recipe for CAD/DXF vector imports, which
  also honours the scene shift.
- ``3DSC4Metashape`` and ``3DSC4RealityCapture`` — pipelines that
  typically produce the multi-tile ``.obj`` datasets handled by this
  recipe.
