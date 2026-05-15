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

The 3DSC Metashape Tools menu is organized into four categories.

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


Utility Tools
-------------

**Rename Chunks**
  Renames all chunks sequentially (1_mt, 2_mt, 3_mt, etc.) for better organization.

  **Use Case:** After importing many tiles, simplify chunk management

**LOD Generator**
  *(Planned feature - not yet implemented)*

  Will generate Level of Detail (LOD) versions directly in Metashape.


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

**Version 1.5.2** (Current)
  - Single-file architecture (``3DSC_MS_GUI.py``)
  - LOCAL coordinate system support
  - Fixed messageBox API errors
  - Float parsing for SHIFT.txt
  - iPad feature experimental (disabled by default)

**Version 1.5.1**
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
  https://github.com/[repository]/3DSC-for-Metashape

**Part of:**
  Extended Matrix Framework
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
