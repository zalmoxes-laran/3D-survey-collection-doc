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

The 3DSC Metashape Tools menu is organized into these categories:
**Shift**, **Import**, **Texturing**, **Export**, **Workflow** and
**Utility**.

Shift Tools
-----------

The **Shift** submenu manages a *global coordinate shift* that is reused by
every import and export operation, so you no longer need to drop a
``SHIFT.txt`` file in each model folder.

**Load Global Shift File**
  Loads a ``shift.txt`` (``CRS X Y Z``) and stores it as the active global
  shift. Once loaded, every import/export uses it automatically unless a
  local ``SHIFT.txt`` is found in the operated folder.

**Current Shift → …**
  A live menu entry that previews the currently loaded shift
  (``CRS X Y Z``). Selecting it shows the full value and the source file.

**Clear Global Shift**
  Removes the active global shift; operations fall back to per-folder
  ``SHIFT.txt`` or to no shift.

.. note::

   **Shift resolution order** for any import/export: (1) a ``.txt`` file
   found in the operated folder, then (2) the global shift loaded from the
   Shift menu, then (3) no shift. See
   :doc:`/how-to/photogrammetry/prepare-with-metashape` for configuration.

Import Tools
------------

**Import Multiple Models**
  Imports multiple OBJ/PLY/DAE files, creating one chunk per model.

  **Workflow:**

  1. Prepare a folder with segmented mesh tiles from Blender
  2. Add SHIFT.txt if coordinate transformation is needed
  3. **3DSC Metashape Tools > Import > Import Multiple Models**
  4. Select the folder containing models
  5. Script creates one chunk per tile

  **Features:**

  - Supports OBJ, PLY, and COLLADA (DAE) formats
  - Reads SHIFT.txt automatically if present
  - Maintains original file names as chunk labels
  - Copies sparse point cloud from first chunk (if available)

**Import Single Model with Shift**
  Imports a single 3D model with optional coordinate transformation.

  **Use Case:** Import individual models or test SHIFT.txt configuration

**Import Tiled Models**
  Reimports previously exported tiled models and rebuilds the tiled model structure.

  **Use Case:** Round-trip workflow for tiled model editing


Texturing Tools
---------------

**Texturize Models**
  Applies automatic texturing using the Demetrescu-d'Annibale formula.

  For the full formula derivation, worked example and rationale, see
  :ref:`texture-resolution-formula`. The script implements the formula with
  the defaults listed below.

  **Automatic Configuration:**

  - Texture size: 4096×4096 px
  - UV mapping mode: Generic
  - Blending mode: Mosaic
  - Hole filling: Enabled
  - Ghosting filter: Enabled

**Texturize Models (200m² limit)**
  Extended texturing mode for larger models (up to 200 m²).

  **Features:**

  - Caps at 12 textures maximum
  - Prevents excessive texture generation for very large tiles
  - Uses same formula but with area constraint

  **Recommendation:** Use for architectural documentation or large archaeological features

.. admonition:: Texture Resolution Rationale

   The 1.26 mm/texel resolution provides:

   - Sufficient detail for VR visualization
   - Recognition of most archaeological features
   - Balanced file size vs. quality
   - Compatibility with real-time engines (Unreal, Unity, Godot)


Export Tools
------------

**Export Multiple Models**
  Exports all chunks as individual textured OBJ files.

  **Workflow:**

  1. Complete texturing of all chunks
  2. **3DSC Metashape Tools > Export > Export Multiple Models**
  3. Select destination folder
  4. Add SHIFT.txt if coordinate transformation is needed
  5. Script exports OBJ + MTL + textures

  **Output Files:**

  - ``model_mt.obj`` - Mesh geometry
  - ``model_mt.mtl`` - Material definition
  - ``model_mt_tex_0.jpg`` - Texture images (multiple if needed)

**Export Single Model with Shift**
  Exports the active chunk as a single textured OBJ file.

**Export Tiled Models**
  Exports Metashape tiled models as individual tile files.

**Cut Giant Mesh into Blocks (with Shift)**
  Segments a large mesh **directly in Metashape** (no Blender round-trip
  required). Internally builds a tiled model sized from a target block area
  (m²) and exports each tile as an OBJ block.

  **Options dialog:**

  - **Block plan area (m²)** — target size per block (default 80)
  - **Run STEP1 now** — prepare/flag LOD0 before cutting
  - **Output mode** — one chunk per block (recommended) or all blocks in one chunk
  - **Grid naming** — name blocks ``block_xNNN_yNNN`` instead of ``block_NNNN``
  - **Export temporary PNG textures** during the cut (slower)
  - **Delete temporary files** after block import
  - **Rebuild tiled model** with the current area settings
  - **Output folder** for the generated ``*_workflow_blocks`` directory

  This tool is STEP2 of the guided workflow below.

**Workflow Export Blocks (Textured First)**
  Exports the blocks produced by the guided workflow, enforcing that each
  block has been textured first (STEP3). See *Guided Workflow* below.

**Export Undistorted Images (Active Chunk)**
  Exports undistorted copies of the active chunk's photos (using the initial
  calibration) into a ``*_undistorted`` folder. Useful for re-texturing in
  external engines or for archival of the corrected imagery.


Guided Workflow (STEP1–STEP5)
-------------------------------

The **Workflow** submenu chains the tools above into a repeatable
"giant mesh → textured blocks" pipeline. It keeps internal state (LOD0
chunk, generated block chunks, textured flags) so each step knows what the
previous one produced.

Two setup actions precede the numbered steps: the (optional) **STEP0** global
shift (Shift menu) and the *prerequisite* of having a high-resolution mesh
built with Metashape's own tools (align photos → build mesh). This is why the
guided workflow's first tool command is STEP1.

**STEP1 — Prepare or Flag LOD0**
  Flags the active chunk's mesh as LOD0, or optionally creates a decimated
  LOD0 copy at a chosen polygon density (polygons per m², default 10000).

**STEP2 — Cut Mesh into Blocks (Options)**
  Same as *Cut Giant Mesh into Blocks* above; opens the options dialog and
  produces one chunk per block (recommended).

**STEP3 — Texturize Workflow Blocks**
  Runs the Demetrescu-d'Annibale texturing on the block chunks generated in
  STEP2 and marks them as textured.

**STEP4 — Generate LODs + Normal Maps (Experimental)**
  Creates LOD1/LOD2 decimated copies of each block (configurable ratios) and,
  when supported by the Metashape API, builds normal maps and preserves
  boundaries.

**STEP5 — Export Workflow Blocks**
  Exports the textured blocks to OBJ, optionally applying the shift and
  writing a ``shift.txt`` alongside the output. Refuses to export blocks that
  were not textured in STEP3.

.. admonition:: Blender-first vs Metashape-first

   The guided workflow lets you **segment in Metashape** instead of Blender.
   Both approaches are valid; the walkthrough in
   :doc:`/how-to/photogrammetry/prepare-with-metashape` documents them side by
   side and explains when to prefer each.


Utility Tools
-------------

**Rename Chunks**
  Renames all chunks sequentially (1_mt, 2_mt, 3_mt, etc.) for better organization.

  **Use Case:** After importing many tiles, simplify chunk management

**LOD Generator**
  *(Placeholder in the Utility menu — not yet implemented.)*

  In-Metashape LOD generation is currently available through
  **Workflow > STEP4 Generate LODs + Normal Maps (Experimental)**, which
  operates on the blocks produced by the guided workflow.


Texture Resolution Formula
==========================

The **Demetrescu-d'Annibale formula** drives the texturing script. The full
derivation, worked example, reference table and rationale live in the
explanation section as the single source of truth:

- :ref:`texture-resolution-formula`

The implementation here calls the formula with the variables:

- ``x_res_a_terra`` → target ground resolution in mm (default: 1.26 mm/texel)
- ``tex`` → texture page resolution in pixels (default: 4096)
- ``ratio`` → surface coverage efficiency factor (default: 0.6)
- ``area_model`` → mesh surface area in m² (computed from the imported mesh)


Python API Reference
====================

**Key Classes and Methods:**

.. code-block:: python

   # Metashape Python API usage in 3DSC tools

   import Metashape as ps

   # Import model with shift
   chunk.importModel(
       path=model_path,
       format=ps.ModelFormat.ModelFormatOBJ,
       shift=ps.Vector([x, y, z]),
       crs=ps.CoordinateSystem("EPSG::32633")  # optional
   )

   # Build UV mapping
   chunk.buildUV(
       mapping_mode=ps.GenericMapping,
       page_count=6,  # number of texture pages
       texture_size=4096
   )

   # Build texture
   chunk.buildTexture(
       blending_mode=ps.MosaicBlending,
       texture_size=4096,
       fill_holes=True,
       ghosting_filter=True
   )

   # Export model
   chunk.exportModel(
       path=export_path,
       format=ps.ModelFormat.ModelFormatOBJ,
       shift=ps.Vector([x, y, z]),
       crs=ps.CoordinateSystem("EPSG::32633"),  # optional
       texture_format=ps.ImageFormat.ImageFormatJPEG,
       save_texture=True,
       save_uv=True,
       save_normals=True
   )

**Coordinate System Handling:**

.. code-block:: python

   # Local coordinates (no CRS)
   chunk.importModel(
       path=model_path,
       shift=ps.Vector([16000, 29000, 0])
       # No crs parameter
   )

   # Geographic coordinates (with EPSG)
   chunk.importModel(
       path=model_path,
       shift=ps.Vector([500000, 4500000, 0]),
       crs=ps.CoordinateSystem("EPSG::32633")
   )


Version History
===============

**Version 1.7.0** (Current)
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
