.. _3DSC4Metashape:

=============================
3DSC for Metashape
=============================

**3DSC for Metashape** is a Python script toolkit that integrates Agisoft Metashape with the 3D Survey Collection (3DSC) workflow in Blender. It enables high-resolution texture generation on segmented photogrammetric models using the **Demetrescu-d'Annibale texture resolution formula** published in `Demetrescu et Alii 2026 <https://doi.org/10.3390/rs18020203>`__

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

The 3DSC for Metashape tools bridge the gap between Blender's geometric segmentation capabilities and Metashape's photogrammetric texturing engine. This integration allows users to:

- Import segmented mesh tiles from Blender into Metashape
- Automatically calculate optimal texture resolution based on model area
- Apply high-resolution textures (1.26 mm/texel) to multiple tiles
- Export textured models with coordinate transformation support
- Maintain Extended Matrix (EM) folder structure compatibility

.. figure:: img/3dsc_metashape_workflow.png
   :width: 800
   :align: center 
   
   *Complete workflow from Blender segmentation to Metashape texturing*

Installation
============

**Requirements:**

- Agisoft Metashape Professional (version 1.6 or later)
- Python-enabled Metashape license
- 3DSC Blender Add-on (for model preparation)

**Installation Steps:**

1. Download the **3DSC for Metashape** package from GitHub:
   
   https://github.com/[repository]/3DSC-for-Metashape

2. Extract the ZIP file to a known location (e.g., Desktop or Documents)

3. In Metashape, go to **Tools > Run Script**

4. Navigate to the extracted folder and select ``3DSC_MS_GUI.py``

5. The **3DSC Metashape Tools** menu will appear in the Metashape menu bar

.. figure:: img/3dsc_menu_metashape.png
   :width: 400
   :align: center 
   
   *3DSC Metashape Tools menu in Agisoft Metashape*

.. admonition:: Single-File Solution

   Version 1.5.2 consolidates all functionality into one file: ``3DSC_MS_GUI.py``
   
   Previous multi-script versions (import_multiple_models.py, texturize_it.py, etc.) 
   are deprecated and can be removed.


SHIFT.txt Configuration
========================

The **SHIFT.txt** file controls coordinate transformation during import and export operations.

File Format
-----------

The SHIFT.txt file must be placed in the same folder as your 3D models with the following format:

.. code-block:: text

   CRS X Y Z

Where:

- **CRS**: Coordinate Reference System or special keyword
- **X, Y, Z**: Shift values (can be integers or decimals)

.. admonition:: Important

   - Use **spaces** to separate values (not commas or tabs)
   - File must contain exactly one line with 4 values
   - Decimal values are supported: ``16000.0`` or ``16000`` both work

Coordinate System Options
--------------------------

**1. Local Coordinates (Non-Georeferenced)**

For models in local coordinate systems without geographic reference:

.. code-block:: text

   LOCAL 16000.0 29000.0 0.0

Alternative keywords: ``NONE``, ``LOCAL_CS``

✅ **Effect**: Applies translation shift only, without setting a coordinate system

**Use Cases:**

- Models exported from Blender with high local coordinates
- Archaeological site models with arbitrary origin points
- Models that need coordinate normalization for visualization


**2. Geographic Coordinates (EPSG)**

For georeferenced models with known coordinate systems:

.. code-block:: text

   EPSG::32633 500000.0 4500000.0 0.0

✅ **Effect**: Applies shift AND sets the coordinate reference system

**Common EPSG Codes:**

- ``EPSG::32633`` - UTM Zone 33N, WGS84
- ``EPSG::32632`` - UTM Zone 32N, WGS84
- ``EPSG::3004`` - Monte Mario / Italy zone 2
- ``EPSG::4326`` - WGS84 Geographic (lat/lon)
- ``EPSG::3857`` - Web Mercator (for web mapping)

**Use Cases:**

- Models for integration with GIS software (QGIS, ArcGIS)
- Georeferenced archaeological sites
- Urban planning and architectural documentation
- Integration with cadastral or topographic data

Selection Guide
---------------

.. list-table::
   :widths: 40 30 30
   :header-rows: 1

   * - Situation
     - SHIFT.txt Format
     - Example
   * - Blender export with local coords
     - ``LOCAL``
     - ``LOCAL 16000.0 29000.0 0.0``
   * - High coordinates to normalize
     - ``LOCAL``
     - ``LOCAL 16000.0 29000.0 100.0``
   * - Georeferenced UTM model
     - ``EPSG::xxxxx``
     - ``EPSG::32633 500000.0 4500000.0 0.0``
   * - Export for GIS integration
     - ``EPSG::xxxxx``
     - ``EPSG::3004 1000000.0 2000000.0 0.0``

.. admonition:: Remember

   All 6 import/export tools in 3DSC for Metashape support both LOCAL and EPSG options.


Tool Reference
==============

The 3DSC Metashape Tools menu is organized into four categories:

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
  
  **Formula:**
  
  .. math::

     N_{\text{tex}} = \frac{(10000 / r_{\text{texel}})^2}{t_{\text{res}}^2 \times ratio}
  
  Where:
  
  - :math:`r_{\text{texel}}` = target resolution in mm/texel (default: 1.26 mm)
  - :math:`t_{\text{res}}` = texture resolution in pixels (default: 4096)
  - :math:`ratio` = surface coverage ratio (default: 0.6)
  
  **Example Calculation:**
  
  For a 100 m² tile with 1.26 mm/texel resolution:
  
  .. math::

     N_{\text{tex}} = \frac{(10000 / 1.26)^2}{4096^2 \times 0.6} \approx 6
  
  **Result:** 6 textures at 4096×4096 pixels
  
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


.. _prepare-survey-metashape:

Complete Workflow Example
==========================

This example demonstrates the complete pipeline from Blender segmentation to textured model export.

Phase 1: Model Preparation in Blender
--------------------------------------

**1.1 Segment High-Resolution Mesh**

Using 3DSC Blender Add-on:

1. Import decimated photogrammetric mesh (1000 poly/m²)
2. Open **3DSC > Segmentation** panel
3. Set **Area (m²)**: 100 (creates 100 m² tiles)
4. Click **Cutter Set** to generate grid
5. Adjust grid position if needed
6. **Trim All** to segment mesh into tiles

**1.2 Export Tiles**

1. Select all segmented tiles
2. **File > Export > Wavefront (.obj)**
3. Save to Extended Matrix structure:
   
   ``05_RB/03_Model_Library/[ModelName]/meshpoly/``

4. Export settings:
   
   - ✅ Selection Only
   - ✅ Objects as OBJ Objects
   - ✅ Write Materials
   - ⬜ Write Normals (optional)

.. figure:: img/blender_segmentation_export.png
   :width: 700
   :align: center 
   
   *Blender segmentation and export to meshpoly folder*


Phase 2: Texturing in Metashape
--------------------------------

**2.1 Prepare Metashape Project**

1. Open photogrammetric project with:
   
   - ✅ Aligned cameras
   - ✅ Sparse point cloud
   - ⬜ Dense cloud (not required)
   - ⬜ Mesh (delete if present - we'll import tiles)

2. **File > Save As** to create texturing project:
   
   ``05_RB/02_PROCESSING/metashape/project_texturing.psx``

**2.2 Import Segmented Tiles**

1. **3DSC Metashape Tools > Import > Import Multiple Models**

2. Navigate to ``05_RB/03_Model_Library/[ModelName]/meshpoly/``

3. Select folder (will auto-detect OBJ files and SHIFT.txt if present)

4. Metashape creates one chunk per tile

.. figure:: img/metashape_chunks_import.png
   :width: 800
   :align: center 
   
   *Metashape workspace after importing 25 tiles - one chunk per tile*

**2.3 Apply Automatic Texturing**

1. **3DSC Metashape Tools > Texturing > Texturize Models**

2. Script processes all chunks automatically:
   
   - Calculates optimal texture count per tile area
   - Generates UV mapping
   - Builds high-resolution textures
   - Displays progress in console

3. Wait for completion (can take 5-10 minutes per tile depending on photo count)

.. figure:: img/metashape_texturing_progress.png
   :width: 700
   :align: center 
   
   *Console output showing texture calculation and progress*

**2.4 Verify Results**

Check each chunk for:

- ✅ Complete texture coverage
- ✅ No visible seams
- ✅ Proper color/lighting
- ⬜ Ghost artifacts (adjust photo selection if needed)

**2.5 Export Textured Models**

1. **3DSC Metashape Tools > Export > Export Multiple Models**

2. Select destination folder:
   
   ``05_RB/03_Model_Library/[ModelName]/meshpolytex/``

3. Add SHIFT.txt if using coordinate transformation

4. Metashape exports all chunks to OBJ format with textures

.. figure:: img/metashape_export_folder.png
   :width: 700
   :align: center 
   
   *meshpolytex folder with exported tiles and textures*


Phase 3: LOD Generation in Blender
-----------------------------------

**3.1 Import Textured Tiles**

1. Open Blender (new file or continue from Phase 1)
2. **File > Import > Wavefront (.obj)**
3. Navigate to ``meshpolytex/`` folder
4. Select all textured OBJ files
5. Import with:
   
   - ✅ Split by Object
   - ✅ Image Search (finds textures)

**3.2 Create LOD Structure**

Using 3DSC LOD Generator:

1. Select all imported tiles
2. **3DSC > LOD Generator**
3. Set **LOD 0 (set as)** for reference model
4. Configure:
   
   - **Number of LODs**: 2 (LOD1, LOD2)
   - **Decimation ratio**: 0.5 for LOD1, 0.25 for LOD2
   - **Texture resolution**: 2048 for LOD1, 1024 for LOD2

5. Set output folder:
   
   ``05_RB/03_Model_Library/[ModelName]/[ModelName]_RB.blend``

6. **Generate LODs**

.. figure:: img/lod_structure.png
   :width: 600
   :align: center 
   
   *LOD collection structure in Blender*


Integration with Extended Matrix
=================================

**EM Folder Structure Integration:**

.. code-block:: text

   05_RB/                              # Reality-Based Data
   ├── 01_RAW/
   │   └── photos/                     # Original photos
   ├── 02_PROCESSING/
   │   └── metashape/
   │       ├── project.psx             # Original photogrammetric project
   │       └── project_texturing.psx   # Texturing project (3DSC workflow)
   └── 03_Model_Library/
       └── [ModelName]/
           ├── meshpoly/               # ← Blender exports HERE
           ├── meshpolytex/            # ← Metashape exports HERE
           └── [ModelName]_RB.blend    # ← Final Reality-Based file

**Workflow Position:**

3DSC for Metashape sits between geometric preparation (Phase 1-2 of Digital Replica workflow) and stratigraphic annotation (Phase 6):

1. **Phase 1-2**: High-res mesh → decimation → segmentation (Blender + 3DSC)
2. **Phase 3**: Texturing tiles (Metashape + 3DSC for Metashape) ← **YOU ARE HERE**
3. **Phase 4**: LOD generation (Blender + 3DSC)
4. **Phase 6**: Stratigraphic annotation (Blender + Extended Matrix)

.. seealso::

   For the complete Digital Replica workflow, see :doc:`digital_replica_preparation`


Troubleshooting
===============

Common Issues and Solutions
---------------------------

**Issue: "wrong crs definition string"**

**Cause:** Invalid coordinate system specification in SHIFT.txt

**Solution:**

- For local coordinates, use: ``LOCAL 16000.0 29000.0 0.0``
- For georeferenced, verify EPSG code: ``EPSG::32633 500000.0 4500000.0 0.0``
- Check for typos in EPSG number

**Issue: "invalid literal for int() with base 10: '16000.0'"**

**Cause:** Older script version doesn't handle decimal values

**Solution:**

- Update to ``3DSC_MS_GUI.py`` version 1.5.2 or later
- Latest version automatically handles both integers and decimals

**Issue: "messageBox() takes exactly 1 argument (2 given)"**

**Cause:** Using outdated script version with incorrect Metashape API calls

**Solution:**

- Download and use ``3DSC_MS_GUI.py``
- Do not use old individual scripts (import_multiple_models.py, etc.)

**Issue: Models import at wrong position**

**Possible Causes:**

1. SHIFT.txt values are incorrect
2. Coordinate system mismatch between Blender and Metashape

**Solutions:**

- Verify shift direction (positive vs negative values)
- Check if models need ``LOCAL`` instead of ``EPSG``
- Test with zero shift first: ``LOCAL 0.0 0.0 0.0``

**Issue: Textures are too small / too large**

**Cause:** Model area doesn't match expected dimensions

**Check:**

1. Verify model is in meters (not millimeters or other units)
2. Check model area in Metashape (right-click chunk → Properties)
3. For very large models (>200m²), use "Texturize Models (200m² limit)"

**Issue: Excessive texture generation (>20 textures per tile)**

**Cause:** Model area is too large for standard formula

**Solution:**

- Use **Texturize Models (200m² limit)** instead
- Caps at 12 textures maximum
- Or resegment model into smaller tiles in Blender

**Issue: Missing textures in export**

**Check:**

1. Texturing completed for all chunks (check progress in Metashape console)
2. Export folder has write permissions
3. Sufficient disk space for texture files

**Issue: Script menu doesn't appear**

**Cause:** Python not enabled or script not loaded correctly

**Solutions:**

1. Verify Metashape Professional license (Standard doesn't support Python)
2. **Tools > Run Script** → select ``3DSC_MS_GUI.py``
3. Check Metashape console (F8) for error messages
4. Try restarting Metashape


Performance Optimization
------------------------

**For Large Projects (>50 tiles):**

1. **Disable unnecessary chunks** during texturing to save RAM
2. **Process in batches**:
   
   - Import 10-15 tiles at a time
   - Texture batch
   - Export batch
   - Remove chunks, import next batch

3. **Reduce photo count**:
   
   - Use only photos with optimal lighting
   - Disable blurred images
   - Align cameras once, then disable photos before texturing

4. **Texture Settings:**
   
   - Start with 2048×2048 textures for testing
   - Switch to 4096×4096 for final export
   - Use JPEG export format to reduce file size (set in export options)

**Memory Management:**

- Each 100m² tile with 6×4096px textures ≈ 150-200 MB RAM during processing
- For 50 tiles: expect 8-10 GB RAM usage minimum
- Close other applications during batch texturing


Technical Reference
===================

Texture Resolution Formula
--------------------------

The **Demetrescu-d'Annibale formula** calculates texture requirements based on:

**Input Parameters:**

- ``x_res_a_terra``: Target ground resolution in mm (default: 1.26 mm/texel)
- ``tex``: Texture resolution in pixels (default: 4096)
- ``ratio``: Coverage efficiency factor (default: 0.6)
- ``area_model``: Mesh surface area in m²

**Calculation:**

.. code-block:: python

   numtex = pow((10000 / x_res_a_terra), 2) / (tex * tex * ratio)
   numtex_x_area = (numtex * area_model) / 100
   tex_num = max(1, round(numtex_x_area, 0))

**Example Values:**

.. list-table::
   :widths: 20 20 20 20 20
   :header-rows: 1

   * - Area (m²)
     - Textures (4096px)
     - Total Pixels
     - Est. File Size
     - Resolution
   * - 10
     - 1
     - 16.7 MP
     - 15 MB
     - 1.26 mm/px
   * - 50
     - 3
     - 50.3 MP
     - 45 MB
     - 1.26 mm/px
   * - 100
     - 6
     - 100.6 MP
     - 90 MB
     - 1.26 mm/px
   * - 200
     - 12 (capped)
     - 201.3 MP
     - 180 MB
     - 1.26 mm/px

.. admonition:: Formula Rationale

   The formula is calibrated for:
   
   - **Archaeological documentation**: Sufficient detail to identify tool marks, inscriptions
   - **VR applications**: Balance between visual quality and performance
   - **Real-time engines**: Texture sizes compatible with game engines
   - **Storage efficiency**: Avoids excessive file sizes for typical projects


Python API Reference
--------------------

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

   **Related Tools:**
   
   - :doc:`3DSCstructure` - 3DSC Blender Add-on documentation
   - :doc:`reference/tools/tsm` - Texture Smart Mapping system
   - :doc:`digital_replica_preparation` - Complete digital replica workflow
   
   **External Resources:**
   
   - `Agisoft Metashape Python API <https://www.agisoft.com/pdf/metashape_python_api_2_0_0.pdf>`_
   - `Extended Matrix Framework <https://www.extendedmatrix.org>`_
   - `3DSC GitHub Repository <https://github.com/zalmoxes-laran/3D-survey-collection>`_
