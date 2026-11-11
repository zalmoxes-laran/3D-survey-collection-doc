.. _3DSC4Metashape:

============================================
3DSC for Metashape — tool reference
============================================

**3DSC for Metashape** is a Python-script toolkit that integrates Agisoft
Metashape with the 3D Survey Collection (3DSC) workflow in Blender. It
enables high-resolution texture generation on segmented photogrammetric
models using the **Demetrescu-d'Annibale texture resolution formula**
published in `Demetrescu et Alii 2026
<https://doi.org/10.3390/rs18020203>`__.

This page is the parameter and API reference for the tool. For the
workflow-oriented walkthrough (install, SHIFT.txt configuration, complete
end-to-end example, troubleshooting), see
:doc:`/how-to/photogrammetry/prepare-with-metashape`.

.. contents:: On this page
   :local:
   :depth: 2


Tool Reference
==============

The **3DSC Metashape Tools** menu follows the order of the work: steps 0–8,
then *Utility* and *Help*. Every panel opens without loading meshes; the
measures it needs are taken on request and kept in the project.

0 · Operator (ORCID)
--------------------

**ORCID iD** (optional, checked with ISO 7064 MOD 11-2) and **name**,
remembered on this computer and written as the declared operator in the stamp
of every export. **Ask again at every export** restores the old question at
each export. Empty = anonymous: the stamp names the software only.

1 · Shift
---------

Loads a ``SHIFT.txt`` (``CRS X Y Z``; ``LOCAL``/``NONE``/``LOCAL_CS`` or an
``EPSG::`` code), shows the file and the values, **Clear** removes it. The
shift is saved in the project (``doc.meta["3dsc_shift_line"]``) and shown in
the menu. Every import and export uses it. See :ref:`shift-coordinates`.

2 · Import
----------

**Models…**

- files or a folder (OBJ, PLY, FBX, DAE, STL, 3DS, glTF); a ``SHIFT.txt`` in
  the folder is offered as the shift;
- **Shift** on/off (on by default);
- **One chunk per model, from the master** or **All models in one chunk**;
- **Master**: the chunk copied for every model. *Create master from the
  active chunk* makes it: photos and tie points only
  (``chunk.copy(items=[TiePointsData])``), flagged ``3dsc_master`` in its meta.

**Photos from Another Project…** — brings a camera group, the selected, the
enabled or all cameras of a chunk of another project into the active chunk,
with calibration, marker projections, masks and camera reference; nothing is
aligned.

3 · Masters
-----------

An inventory of the models of a chunk, then what is missing.

- **Chunk** and **Reference chunk** (its surface is used when the chunk has
  no mesh yet);
- **Densities**: texturable (10 000 faces/m²) and tileable (1 000 faces/m²);
- table: model, faces, faces/m², texture, part in the chain;
- **Measure**: faces of every model and the surface of the lightest (kept in
  ``3dsc_faces`` and ``3dsc_area_m2``);
- report and **Make what is missing**: decimations from the highest model
  (``decimateModel(model=…, replace_asset=False)``), listed and confirmed
  first; the new models are ``M_texturable_<d>`` and ``M_tileable_<d>``.

Rules: the highest model is the one to clean; above the texturable density it
is the geometric super master; when no model reaches it, the highest is kept
for the tileset; LOD0 is made only from a denser model. A model within ±25 %
of a target density counts as that master.

4 · Blocks
----------

- **Chunk** (its active model is cut) and **Block plan area** (m²; the side
  is its square root);
- **Grid orientation**: project grid · selected line · two markers · bearing
  typed (degrees clockwise from grid north) · fit to the mesh (minimum-area
  rectangle of the footprint) · north;
- **Preview the grid in the view** / **Remove preview**: the cells holding
  mesh as shapes of the group «3DSC grid preview»;
- **Save this grid as the project grid** (``doc.meta["3dsc_grid"]``: grid
  CRS, origin, side, bearing);
- **Small tiles under**: a share of the block area (33 % by default), m² of
  ground (between 0 and the block area) or faces; each small tile is merged
  into a tile that shares a side — the cell next door first, then the largest
  — or only flagged. Ground is the plan area of the faces;
- **Output**: the blocks as models of one new chunk (``<chunk>_blocks``) ·
  one chunk per block · files only; **Master** for the new chunk(s);
- **Folder**: ``<chunk>_workflow_blocks`` with the blocks, ``metadata.xml``
  and, for a turned grid, ``grid_crs.wkt``.

The cut is Metashape's Block Model (``buildModel(split_in_blocks=True,
blocks_size=…)``). A turned grid is passed as ``blocks_crs`` — a local oblique
Mercator (``Oblique_Mercator``, EPSG method 9815) centred on the site with
scale 1 — and ``blocks_origin``; the chunk's own coordinate system and
transform are never changed. Blocks are named ``block_xNNN_yNNN`` from their
cell, counted from the grid origin, so the project grid gives the same names
in every epoch. The cut stops when two blocks are identical or the blocks add
up to more than 1.5 × the faces of the source.

5 · Texturing
-------------

- **Texel** (1.26 mm), **Atlas** (2048/4096/8192 px), **UV ratio** (0.6),
  **Max pages per chunk** (none by default);
- one row per model: area, faces, pages, texel reached, memory (raw RGB);
- *Select all*, *None*, *Untick masters*, *Measure*;
- with many chunks: **Work in a new project** with the reference chunk and
  the ticked ones (``Document.append`` + ``save``; the open project is
  unchanged).

Each ticked model becomes the active one, then ``buildUV(page_count=…)`` and
``buildTexture(MosaicBlending)``; the values used go to ``model.meta["3dsc_dd"]``.
A progress window shows the model N of M, done and left, the current stage, the
time spent and left (weighted by pages, ``ms_progress.py``) and the expected
end; *Stop after this one* ends the batch between two models.

6 · LODs + Normal Maps
----------------------

LOD1 and LOD2 ratios (0.5 and 0.25): each block is decimated from its own
faces. Blocks held as models get ``<block>_LOD1`` and ``<block>_LOD2`` in the
same chunk.

7 · Tileset
-----------

- **Chunk**, **Tiled model**, or *build it now* from the active model
  (``buildTiledModel(source_data=ModelData)``, pixel size from the texel);
- **Screen space error** (presets full detail 16 · web 8 · mobile 4): written as
  each tile's ``geometricError`` = value × texel of the level; tiles and
  textures are the same whatever the value. In a viewer whose threshold is 16
  px a texel is drawn on up to 16 / value pixels;
- **Tileset version** 1.1/1.0, **Textures** KTX2/JPEG, **Draco**,
  **tileset transform**, **clip to boundary**, **folder depth**;
- **Heights**: correction onto EGM2008 for this export only, from
  Metashape's geoid or a JSON table ``{marker: N}``; marker heights become
  H + N − Δdatum, then ``updateTransform``; markers and transform are put back
  after the export;
- **File** ``.3tz`` or folder.

After the export the written file is read back: tiles per level, primitives
per tile, size, root position (latitude, longitude, ellipsoidal height).

8 · Export
----------

**Blocks** (textured, with LODs; OBJ with UV and textures), **Models** (one
file per chunk), **Active model with shift**, **Undistorted images** of the
active chunk. Every file is stamped (``<file>.stamp.json``, dtcstamp 0.1.3);
the private address of the master in the project goes in
``<file>.hints.json``.

Utility and Help
----------------

**Rename Chunks…**: pattern with ``{n}``, ``{name}``, ``{model}``, start,
digits, find/replace, preview; acts on the selected chunks or on all.
**Flag LOD0** (the former STEP1). **Help**: this documentation; *About* with
the rule and the references.


Texture Resolution Formula
==========================

The **Demetrescu-d'Annibale formula** drives the texturing script. It was
published as Equation (1) in `Demetrescu et al. 2026
<https://doi.org/10.3390/rs18020203>`__. The full derivation, worked example,
reference table and rationale live in the explanation section as the single
source of truth:

- :ref:`texture-resolution-formula`

The implementation here calls the formula with the variables (published
notation → code name):

- :math:`r_{\text{target}}` → ``texel_mm`` — side of one texel on the
  surface (default: 1.26 mm)
- :math:`s_{\text{tex}}` → ``atlas_px`` — texture atlas dimension in pixels
  (default: 4096)
- :math:`r_{\text{uv}}` → ``uv_ratio`` — UV-space utilization efficiency
  (default: 0.6)
- :math:`A_{\text{tile}}` → ``area_m2`` — surface area of the model in m²,
  from ``model.area()``

The functions are in ``ms_dd.py``: ``pages_for(area)``, ``texel_for(area,
pages)`` (the rule read backwards) and ``simulate(area, max_pages=…)``.


Code Reference
==============

``3DSC_MS_GUI.py`` holds the menu and the work done in Metashape;
``ms_panels.py`` the panels (PySide2). The logic that does not need Metashape
lives in pure modules, tested with ``python3 -m unittest discover tests``:

- ``ms_dd.py`` — the Demetrescu-D'Annibale rule and the master densities
- ``ms_masters.py`` — the inventory of the masters
- ``ms_grid.py`` — the turned grid: minimum-area rectangle, layout, oblique
  Mercator definition, cell names
- ``ms_blocks.py`` — checks, names and small tiles of a cut
- ``ms_tileset.py`` — reading back an exported tileset
- ``ms_appender.py`` (+ ``ms_append_ms.py``, ``ms_append_gui.py``) — photos
  from another project
- ``dtc_stamp_ms.py`` + ``vendor/dtcstamp.py`` — the stamp of every export

Notes measured on Metashape 2.3.2: a model built by Metashape has an identity
``Model.transform`` and internal vertices, an imported one carries its own
translation to geocentric coordinates; several models of one chunk are
textured one at a time by making each the active model; block files cut with
a custom ``blocks_crs`` have no ``metadata.xml``, so 3DSC exports each block
model again in the chunk's coordinate system.


Version History
===============

**Unreleased** (after 1.7.0)
  - Menu in steps 0–8 with panels; operator and shift remembered
  - **Masters** as an inventory of the chain (geometric · texturable 10 000/m²
    · tileable 1 000/m²), decimations confirmed before running
  - **Blocks** on a grid turned with the monument (line, markers, bearing,
    mesh), previewed in the view; one **project grid** for every epoch;
    blocks as models of one chunk
  - **Texturing** one model at a time; the 200 m² cap removed
  - **Tileset** export with screen space error, EGM2008 heights for one
    export, check read from the file
  - Removed: Import Single/Multiple/Tiled Models, Export Tiled Models,
    Texturize 200 m², LOD Generator, iPad import

**Version 1.7.0**
  - Version numbering realigned with the 3DSC Blender extension (``dsc_tools``)
  - **Global Shift** menu — load a coordinate shift once and reuse it across
    all import/export operations
  - **Guided Workflow** menu (STEP1–STEP5): prepare/flag LOD0 → cut mesh into
    blocks → texturize → generate LODs + normal maps → export
  - **Cut Giant Mesh into Blocks** — in-Metashape segmentation via tiled models
  - **Export Undistorted Images** of the active chunk
  - Single-file architecture (``3DSC_MS_GUI.py``)

**Version 2.1 / 1.5.2** (legacy numbering)
  - Single-file architecture (``3DSC_MS_GUI.py``)
  - LOCAL coordinate system support
  - Fixed messageBox API errors
  - Float parsing for SHIFT.txt
  - iPad feature experimental (disabled by default)

**Version 2.0 / 1.5.1**
  - Graphical user interface
  - Extended texture support (200m² limit)
  - Tiled model import/export
  - iPad AR camera import (experimental)
  - Improved error handling

**Legacy multi-script**
  - Individual Python scripts
  - Basic import/export functionality
  - Original texture formula implementation


Credits and License
===================

**Author:**
  Emanuel Demetrescu
  CNR-ISPC (Consiglio Nazionale delle Ricerche - Istituto di Scienze del Patrimonio Culturale)
  Rome, Italy

**Email:**
  emanuel.demetrescu@gmail.com

**License:**
  GNU General Public License v3 (GPL-3)

**Citation:**

If you use 3DSC for Metashape in your research, please cite:

  Demetrescu, E. (2025). *3DSC for Metashape: High-Resolution Texture Generation
  for Segmented Photogrammetric Models*. Extended Matrix Project.
  https://github.com/zalmoxes-laran/3DSC_Metashape

**Part of:**
  Extended Matrix Ecosystem
  https://www.extendedmatrix.org


.. seealso::

   - :doc:`/how-to/photogrammetry/prepare-with-metashape` — workflow walkthrough
   - :doc:`/reference/panels/index` — 3DSC Blender Add-on panels reference
   - :doc:`/reference/tools/tsm` — Texture Smart Mapping system
   - :doc:`/how-to/digital-replica/index` — Complete digital replica workflow
   - :doc:`/explanation/texture-resolution-formula` — Formula derivation and rationale
   - `Agisoft Metashape Python API <https://www.agisoft.com/pdf/metashape_python_api_2_0_0.pdf>`_
   - `Extended Matrix Framework <https://www.extendedmatrix.org>`_
   - `3DSC GitHub Repository <https://github.com/zalmoxes-laran/3D-survey-collection>`_
