.. _prepare-survey-metashape:

============================================
Prepare a digital replica with Metashape
============================================

This recipe follows **3DSC for Metashape**, the companion of the 3D Survey
Collection (3DSC) for Agisoft Metashape, from an aligned photogrammetric
project to textured blocks, their levels of detail and a Cesium tileset. It
is written for whoever documents a site and has to deliver a *digital
replica*: a model whose geometry, texture and provenance can be checked.

The tool reference (parameters, formula, Python API) is
:doc:`/reference/tools/metashape-tool`; the reasons behind the texture rule
are in :doc:`/explanation/texture-resolution-formula`, those behind the shift
in :ref:`shift-coordinates`.

.. contents:: On this page
   :local:
   :depth: 2


The idea in one paragraph
=========================

A photogrammetric survey produces one heavy mesh. 3DSC for Metashape turns it
into a **chain of masters** that differ only by density, each with a job:

.. list-table::
   :widths: 28 22 50
   :header-rows: 1

   * - Master
     - Density (faces/m²)
     - What it is for
   * - **Geometric super master**
     - above 10 000
     - kept aside: archive, 3D printing, measurement. It is the model you
       **clean** (trees, scaffolding, noise); every lighter master is
       derived from it and inherits the cleaning.
   * - **Texturable master**
     - 10 000
     - the source of the **Cesium tileset** for the web and of the normal maps.
   * - **Tileable master (LOD0)**
     - 1 000
     - cut into **blocks**, textured at about one millimetre per texel,
       then reduced into LOD1, LOD2… for Blender and Extended Matrix.

Two words are kept apart throughout: a **block** is a piece of mesh physically
cut (one file per block); the **tileset** is Metashape's own quadtree,
exported as 3D Tiles.

.. Screenshot to add: the 3DSC Metashape Tools menu (steps 0–8, Utility, Help).

.. admonition:: Follow along with an open dataset
   :class: tip

   This walkthrough can be reproduced with a **freely downloadable dataset**:

   **Segni (RM): Acropoli. Rilievo fotogrammetrico** —
   `zenodo.org/records/7463167 <https://zenodo.org/records/7463167>`__
   (DOI `10.5281/zenodo.7463167 <https://doi.org/10.5281/zenodo.7463167>`__,
   licensed CC-BY-NC-SA 4.0).

   You mainly need:

   - ``Segni_Acropoli_Canon6D_24mm.rar`` and/or ``Segni_Acropoli_drone.rar`` —
     the source photographs
   - ``Segni_Acropoli_soluzione_fotogrammetrica.xml`` — the ready-made
     photogrammetric solution (aligned cameras and tie points): import it to
     **skip the long alignment**
   - the accompanying ``.txt`` file — the coordinate **shift** of the site
   - ``Segni_Acropoli_RB.zip`` — the Reality-Based package, showing the
     Extended Matrix ``05_RB`` folder structure


Installation
============

**Requirements**

- Agisoft Metashape **Professional** 2.x (developed and measured on 2.3.2);
  the Standard edition has no Python
- the 3DSC Blender extension, for the Blender side of the work

**Steps**

1. Download the latest release of **3DSC for Metashape** from
   `github.com/zalmoxes-laran/3DSC_Metashape/releases <https://github.com/zalmoxes-laran/3DSC_Metashape/releases>`__
   (the source ``.zip`` of the newest tag) and extract it.
2. Keep the files **together in one folder**: ``3DSC_MS_GUI.py`` loads the
   modules beside it (the panels, the texture rule, the grid, the stamp…).
3. In Metashape: **Tools › Run Script…** and choose ``3DSC_MS_GUI.py``.
4. The **3DSC Metashape Tools** menu appears in the menu bar. Run the script
   again after updating the files.

The menu follows the order of the work:

.. list-table::
   :widths: 8 32 60
   :header-rows: 1

   * - Step
     - Entry
     - What it does
   * - 0
     - Operator (ORCID)…
     - who runs the operations, written in the stamp of every export
   * - 1
     - Shift…
     - one coordinate shift for every import and export, kept in the project
   * - 2
     - Import › Models… / Photos from Another Project…
     - models into copies of the *master*; photos brought from another project
   * - 3
     - Masters…
     - what the chunk has and lacks along the chain; makes what is missing
   * - 4
     - Blocks…
     - cuts the tileable master on a grid turned with the monument
   * - 5
     - Texturing…
     - the Demetrescu-D'Annibale rule, one model at a time
   * - 6
     - LODs + Normal Maps
     - LOD1, LOD2… of every block
   * - 7
     - Tileset…
     - Cesium 3D Tiles (``.3tz``) from the texturable master
   * - 8
     - Export ›
     - blocks, models, the active model, undistorted images
   * -
     - Utility › Rename Chunks… · Help ›
     - names that become file names; this documentation, rule and references


Before you start: operator and shift
====================================

**Operator.** *0 · Operator (ORCID)…* asks once for your ORCID iD (optional)
and name, checks the iD and remembers it on this computer. From then on every
export is stamped with it, without asking again; tick «ask again at every
export» if several people use the same machine. Left empty, the stamps name
the software only.

**Shift.** Georeferenced coordinates are too large for the single-precision
numbers of Blender and of many viewers, so 3DSC works with a shift: a
``SHIFT.txt`` with one line ``CRS X Y Z``.

.. code-block:: text

   EPSG::3004 2312000.0 4614000.0 0.0      georeferenced: shift and coordinate system
   LOCAL 16000.0 29000.0 0.0               local: shift only (also NONE, LOCAL_CS)

*1 · Shift…* loads the file, shows its content and the numbers it read, and
**saves the shift in the project**: it comes back when you reopen the
``.psx``, and the menu shows it in brackets. *Clear* removes it. Use the same
file Blender used for the site, so that both programs speak the same
coordinates.

.. Screenshot to add: the Shift panel with the Segni shift loaded.


Workflow A — blocks cut in Blender
==================================

Choose this path when the blocks are already cut in Blender (3DSC
Segmentation panel), for instance because the cut lines follow walls or
stratigraphic units drawn by hand.

**A.1 Cut and export in Blender.** See :ref:`segmentation`. Export the blocks
as OBJ into ``05_RB/03_Model_Library/<Model>/meshpoly/``, with the site's
``SHIFT.txt`` beside them.

.. figure:: ../../img/blender_segmentation_export.png
   :width: 700
   :align: center

   *Blender segmentation and export to the meshpoly folder*

**A.2 Prepare the Metashape project.** Open the photogrammetric project
(aligned cameras and tie points; a mesh is not needed) and save a copy for
texturing, e.g. ``05_RB/02_PROCESSING/metashape/project_texturing.psx``.

**A.3 Create the master.** Select the chunk of the photos and use
*2 · Import › Models… › Create master from the active chunk*. The master is a
copy holding **only the photos and the tie points**: every model imported
later lands in a copy of it, so it can be textured from the photos without
dragging depth maps, point clouds or other meshes along.

**A.4 Import the blocks.** In the same panel add the files or the
``meshpoly`` folder (a ``SHIFT.txt`` found there is offered as the shift),
leave *Shift* ticked and choose:

- **one chunk per model, from the master** — one chunk per block, as in
  earlier versions;
- **all models in one chunk** — lighter: one chunk holding every block as a
  model of its own (see *Several models in one chunk* below).

.. Screenshot to add: the Import panel with the meshpoly folder and the master.

**A.5 Texture.** Go on with *Texturing* (below, B.5), then *Export › Blocks*
to ``meshpolytex/``, and come back to Blender for the LODs (:ref:`lod-generator`,
:ref:`lod-manager`).


Workflow B — from the mesh to the blocks, in Metashape
======================================================

**B.0 Build and clean the high mesh.** With Metashape's own tools: align (or
import the ready-made solution), build the mesh at high quality, then
**clean it**: vegetation, scaffolding, people, noise at the edges. This is
the moment to work on the geometry, because every lighter master will be
decimated from this one and will inherit what you removed.

B.1 Masters: what is there, what is missing
-------------------------------------------

*3 · Masters…* opens on the chunk and lists its models with their faces,
density and part in the chain. Opening is instant: nothing is loaded. Press
**Measure** once — it counts the faces of every model and measures the
surface on the lightest one (decimations keep the surface), and keeps the
numbers in the project. For a sense of the wait: 40.9 million faces take
about 13 seconds on a recent Mac.

The panel then writes, in plain words, what it found:

- the **highest model is the one to clean**, the base of every decimation;
  above 10 000 faces/m² it is the geometric super master;
- if a model sits near **10 000/m²** it is the texturable master; if none
  reaches that density, the highest is **kept for the tileset** — a
  decimation removes detail, it never adds it;
- if a model sits near **1 000/m²** it is the tileable master (LOD0);
  otherwise it can be decimated from a denser one;
- models lighter than LOD0 are marked as previews or LODs.

*Make what is missing* lists the exact decimations (source, target faces)
and asks before running them; the source model is never changed. When a
chunk has no mesh yet, the **reference chunk** gives the surface, and the
panel tells you how many faces each master will need.

.. admonition:: An example: Templu Mare, 2015
   :class: note

   Three models of 40.9 M, 6.3 M and 0.6 M faces on about 6 040 m². The
   panel says: clean the 40.9 M model and keep it for the tileset (6 800/m²,
   no model reaches 10 000); the 6.3 M model is already LOD0 (1 041/m²);
   the 0.6 M model is lighter than LOD0; nothing to make.

.. Screenshot to add: the Masters panel after Measure, on a real chunk.

Clean the high model again later? Run *Masters* again: the lighter masters of
that level are replaced by new ones, decimated from the cleaned model.

B.2 The master of the photos
----------------------------

As in A.3: *Import › Models… › Create master from the active chunk*, on the
chunk of the photos. You need it once per photo set — once per epoch, if the
site was surveyed more than once.

B.3 Blocks on a grid turned with the monument
---------------------------------------------

*4 · Blocks…* cuts the active model of a chunk — normally the tileable
master — into square blocks of the area you choose (80 m² gives blocks of
8.94 m). Metashape's own block cut lays its grid on the north; a temple
turned by 10° then wastes many half-empty blocks along its sides. 3DSC turns
the grid with the monument and keeps it tight on the mesh.

**Where the angle comes from.** In order of preference:

- **Project grid** — the grid saved on an earlier cut (see B.4);
- **Selected line** — draw a polyline along the walls (*Draw Polyline* in
  the Model view), select it, and the grid takes its direction. This is the
  most direct way to say «this is the axis of the building»;
- **Two markers** along the axis;
- **Bearing typed**, in degrees clockwise from the grid north;
- **Fit to the mesh** — the narrowest rectangle around the footprint of the
  mesh. It is right for a monument modelled on its own; when the mesh
  includes the surrounding terrain, the terrain decides the rectangle and
  the result says little about the building;
- **North** — Metashape's default.

**See it before cutting.** *Preview the grid in the view* draws the cells
that hold mesh as orange outlines in the Model view, in a shape group called
«3DSC grid preview», and writes the angle, where it comes from, and how many
blocks it gives against a north grid. *Remove preview*, *Cancel* and the cut
itself take the outlines away.

.. Screenshot to add: the Templu Mare with the orange grid along the walls.

**The project is never rotated.** The turned grid exists only inside the cut
command (as the coordinate system of the block grid: a local oblique Mercator
centred on the site, scale 1). The chunk keeps its coordinate system and its
position: nothing rotated is ever saved, and the same settings always give
the same blocks. The block files are then written in the chunk's coordinate
system with the usual ``metadata.xml`` (plus ``grid_crs.wkt``, the grid used).

**Small tiles.** Blocks with fewer faces than the threshold (2 000 by
default) are merged into their largest neighbour, or only flagged. The cut
stops, naming the files, if two blocks turn out identical or if all blocks
add up to far more faces than the source.

**Output.**

- **the blocks as models of one new chunk** (default), copied from the
  master: ``<chunk>_blocks`` holds ``block_x001_y001``, ``block_x001_y002``…
- one chunk per block;
- files only, to check or clean them in Blender first.

B.4 More epochs, one grid
-------------------------

Tick **save this grid as the project grid** on the first cut. When you cut
another chunk of the same site — another survey campaign, another
interpretative hypothesis — choose **Project grid**: the cells are the same,
and so are the names. ``block_x003_y002`` is the same piece of ground in 2013
and in 2015, which makes the two epochs comparable block by block, in
Metashape, in Blender and in Extended Matrix.

B.5 Texturing: about one millimetre per texel
---------------------------------------------

*5 · Texturing…* lists **one row per model** (blocks of every chunk, masters,
imported models) with its surface, the texture pages the rule asks for, the
texel they give and the memory they take. Tick what to texture — *Untick
masters* removes the master chunks; *Measure* fills the surfaces still
unknown.

The rule is the Demetrescu-D'Annibale formula (Demetrescu et al. 2026,
`Remote Sensing 18, 203 <https://doi.org/10.3390/rs18020203>`__, Eq. 1):

.. code-block:: text

   pages = round( area · (1000 / texel)² / (atlas² · UV ratio) )

with a texel of **1.26 mm**, atlases of **4096 px** and a UV ratio of **0.6**
(the share of each page the UV islands really fill). A 100 m² block needs
6 pages. A large area needs no cap: set *Max pages per chunk* and the panel
shows the coarser texel you accept instead; leave it empty and the texel stays
at 1.26 mm with more pages. The values used are written in each model's
metadata.

**Several models in one chunk.** Metashape 2.x keeps several models in one
chunk and textures them one at a time: each becomes the active model, gets its
own UV pages and texture, and the others keep theirs. Measured on Templu Mare
2015: two pieces textured in 26 and 16 seconds, each with its own texture,
the models already in the chunk untouched. Separate chunks are needed only
for different photos or alignments — that is, for different epochs.

**Many chunks?** Above a dozen, the panel offers to save a **new project**
holding the reference chunk and the ticked ones: texturing is lighter there,
and the open project stays as it is.

.. Screenshot to add: the Texturing panel with the simulation of a set of blocks.

B.6 LODs and normal maps
------------------------

*6 · LODs + Normal Maps* asks for the LOD1 and LOD2 ratios (0.5 and 0.25 by
default) and decimates **each block from its own faces**: LOD1 has half the
faces of the LOD0 block, LOD2 a quarter. For blocks held as models of one
chunk, the LODs are added to the same chunk (``block_x001_y001_LOD1``…).
Normal maps let the lighter levels keep the surface detail of the
texturable master.

B.7 The Cesium tileset
----------------------

*7 · Tileset…* exports the tiled model of a chunk as **Cesium 3D Tiles**,
directly in a ``.3tz`` archive or in a folder, or builds it first from the
active model (the texturable master), at the texel of the rule.

- **Screen space error** decides how many tiles a viewer draws at a given
  distance: higher means fewer tiles, lighter scenes. Presets: desktop 16,
  web 24, mobile 32. The same error can also be tuned later in the viewer.
- Version 1.1 or 1.0, textures in KTX2 (compressed for the graphics card) or
  JPEG, Draco geometry compression, tileset transform, folder depth, clip to
  boundary shapes.
- **Heights.** When the chunk's coordinate system has no vertical datum and
  its markers carry heights, the panel says so: if those heights are
  orthometric (levelling, benchmarks), the tileset would sit tens of metres
  too low on the globe. The export can move them onto **EGM2008** for that
  export only — marker heights, then the chunk's position — and puts
  everything back exactly afterwards. The undulation N comes from
  Metashape's EGM2008 geoid, if installed, or from a small table
  ``{marker: N}``.
- **Check.** After the export the file itself is read back: tiles per level,
  primitives per tile (each one a draw call), size, and where the root sits
  on the Earth.

B.8 Export
----------

*8 · Export ›* writes the blocks (with their LODs, OBJ with textures), the
models of the chunks one file each, the active model, or the undistorted
photos of the active chunk, always with the shift of the project. Every file
gets a ``<file>.stamp.json`` beside it: what Metashape recorded about the
operations, the photos, the software and the operator.

Typical destination: ``05_RB/03_Model_Library/<Model>/meshpolytex/``. From
there the blocks go into Blender for annotation.


Integration with Extended Matrix
================================

.. code-block:: text

   05_RB/                              # Reality-Based data
   ├── 01_RAW/
   │   └── photos/                     # original photos
   ├── 02_PROCESSING/
   │   └── metashape/
   │       ├── project.psx             # photogrammetric project
   │       └── project_texturing.psx   # texturing project (3DSC)
   └── 03_Model_Library/
       └── <Model>/
           ├── meshpoly/               # blocks cut in Blender (Workflow A)
           ├── meshpolytex/            # textured blocks from Metashape
           └── <Model>_RB.blend        # the Reality-Based file

In the Digital Replica workflow (:doc:`/how-to/digital-replica/index`) this
page covers the masters, the cut and the texturing; Blender takes over for
the LODs of Workflow A and for the stratigraphic annotation.


Troubleshooting
===============

**The menu does not appear.** Metashape Professional is needed (Standard has
no Python). *Tools › Run Script…* on ``3DSC_MS_GUI.py``, with all the files
of the release in the same folder; errors are in the console
(*View › Console*).

**«wrong crs definition string» when loading the shift.** The first word of
``SHIFT.txt`` must be ``LOCAL`` (or ``NONE``, ``LOCAL_CS``) or a code such as
``EPSG::32633``; the four values are separated by spaces.

**Models land in the wrong place.** Check that Blender and Metashape use the
same ``SHIFT.txt``, and that *Shift* is ticked in the Import panel. For a
local model try ``LOCAL 0 0 0`` first.

**Masters makes nothing.** Read its report: no model may be denser than the
master you ask for (a decimation cannot add detail), or the models may not be
measured yet.

**The rotated grid is not along the walls.** *Fit to the mesh* follows the
footprint of the whole mesh, terrain included: draw a line along the walls
and use *Selected line*, or pick two markers.

**«a rotated grid needs a projected CRS».** The chunk must be in a metric,
projected coordinate system (UTM, Gauss-Boaga, Stereo70…), not in latitude
and longitude.

**Too many texture pages.** Check that the model is in metres; for a very
large model set *Max pages per chunk* and accept the coarser texel the panel
shows, or cut it into blocks first.

**The tileset sits below the ground in the viewer.** The heights are
probably orthometric in a coordinate system without vertical datum: tick the
EGM2008 correction in the Tileset panel.

Performance
-----------

- Prefer the blocks as models of one chunk per epoch: no copy of the photos
  for every block.
- With many chunks, texture in a new project holding only the reference chunk
  and the blocks (the Texturing panel offers it).
- Measuring is done once and kept in the project; re-measure after cleaning
  a model.
- Disable blurred or redundant photos before texturing; test at 2048 px
  pages, deliver at 4096.


.. seealso::

   - :doc:`/reference/tools/metashape-tool` — parameters and Python API
   - :doc:`/explanation/texture-resolution-formula` — the Demetrescu-D'Annibale rule
   - :ref:`shift-coordinates` — why and when to shift coordinates
   - :doc:`/how-to/digital-replica/index` — the complete digital replica workflow
   - :doc:`/reference/panels/index` — 3DSC Blender panels
   - `3DSC for Metashape on GitHub <https://github.com/zalmoxes-laran/3DSC_Metashape>`_
   - `3DSC for Metashape on extendedmatrix.org <https://www.extendedmatrix.org/tools/3dsc-metashape/>`_
   - Demetrescu, E., Ferdani, D., Fanini, B., D'Annibale, E., Berto, S.,
     Morretta, S., Rea, R. (2026). Digital Replicas and 3D Virtual
     Reconstructions for Large Excavations in Urban Archaeology: Methods,
     Tools, and Techniques Drawn from the "Metro C" Case Study in Rome.
     *Remote Sensing* 18(2), 203. https://doi.org/10.3390/rs18020203
