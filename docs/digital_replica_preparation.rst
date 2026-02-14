.. _digital_replica_preparation:

========================================
Digital Replica Preparation Workflow
========================================

This workflow describes the complete pipeline for preparing photogrammetric models for use in Blender with 3D Survey Collection (3DSC), optimized for real-time visualization and stratigraphic annotation.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

The **Digital Replica** workflow creates optimized 3D models (called "canvas") with:

- **Constant mesh density**: 1,000 or 10,000 polygons/m²
- **High-resolution textures**: 1.2 mm/texel using a specific formula
- **Multiple LODs** (Levels of Detail) for efficient real-time visualization
- **Optimized structure** for stratigraphic annotation projects

The final output is a Reality-Based (RB) file ready for import into stratigraphic annotation projects using PyArchInit, Extended Matrix, or other tools.

Workflow Steps
==============

Phase 1: High-Resolution Mesh Preparation (Metashape)
-------------------------------------------------------

**1.1 Photo Alignment and Mesh Generation**

Start with a standard photogrammetric project in Agisoft Metashape:

1. Align photos using standard workflow
2. Build dense cloud
3. Generate high-resolution mesh

.. figure:: img/metashape_higres_mesh.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Metashape interface showing high-resolution mesh with ~74M polygons]*

.. admonition:: Note

   The initial high-resolution mesh can contain tens of millions of polygons. This is normal and will be decimated in the next step.

**1.2 Mesh Decimation (Canvas Creation)**

Create the "canvas" - a uniform mesh with constant polygon density:

1. In Metashape, select **Tools > Mesh > Decimate Mesh**
2. Set target face count based on model area:
   
   .. math::

      \text{Target Faces} = \text{Area (m²)} \times 1000

   Example: For 231 m² → 231,000 faces

3. Execute decimation
4. Verify mesh quality (check for holes, flipping geometries)

.. figure:: img/decimated_canvas.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Decimated mesh at 1000 poly/m² showing uniform density]*

.. admonition:: Why 1000 polygons/m²?

   This density provides an optimal balance:
   
   - Sufficient detail to recognize most features
   - Low enough for efficient editing in Blender
   - Compatible with game engines (Unreal, Unity, Godot, O3DE)
   - Avoids flipping geometry artifacts common in very dense meshes

**1.3 Export Canvas Mesh**

1. Select the decimated mesh
2. **File > Export > Export Model**
3. Format: **Wavefront OBJ**
4. Navigate to your EM project structure:
   
   ``05_RB/03_Model_Library/[YourModelName]/meshmono/``
   
   Create the subfolders if they don't exist:
   
   .. code-block:: text

      05_RB/03_Model_Library/[YourModelName]/
      ├── meshmono/          # Single decimated mesh (this export)
      ├── meshpoly/          # Segmented tiles (created later)
      └── meshpolytex/       # Textured tiles (final output)

5. Export to the ``meshmono/`` folder
6. Coordinate system: Use local or georeferenced (note: will affect later steps)

.. admonition:: EM Structure Note

   All intermediate and final mesh outputs are stored within the Model Library 
   (05.03) subfolder structure. This keeps photogrammetric outputs organized 
   and separate from raw data and processing files.

.. figure:: img/export_meshmono.png
   :width: 600
   :align: center
   
   *[SCREENSHOT: Metashape export dialog with OBJ settings]*


Phase 2: Mesh Segmentation (Blender + 3DSC)
---------------------------------------------

**2.1 Import Canvas in Blender**

1. Open Blender
2. Install 3D Survey Collection add-on if not already installed
3. **Import > 3DSC > Import OBJ (Ant File Importer)**
4. Navigate to ``05_RB/03_Model_Library/[YourModelName]/meshmono/``
5. Select the OBJ file

.. figure:: img/blender_import_3dsc.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Blender with 3DSC import panel open, showing EM folder structure]*

.. admonition:: Coordinate Systems

   - **Local coordinates**: Import directly
   - **Georeferenced**: Use the shift file option in 3DSC importer to handle large coordinates

**2.2 Segment with LOD Cutter**

The LOD Cutter tool divides the mesh into manageable tiles:

1. Select the imported mesh
2. Open **3DSC > Segmentation** panel
3. Set **Grid Size** (in m²):
   
   - Recommended: 60-100 m² per tile
   - Formula for grid dimension: :math:`\sqrt{\text{Area}}` (e.g., 8×8m or 10×10m)
   
   .. note::
   
      The grid size should account for both horizontal and vertical surfaces. For architectural models with walls, use smaller tiles (~60 m²) to account for the Z dimension.

4. Click **Cutter set** to generate the cutting grid
5. Adjust grid if needed

.. figure:: img/lod_cutter_grid.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Blender viewport showing segmentation grid overlay on mesh]*

**2.3 Execute Multi-Cutter**

1. Select the target mesh (active object)
2. Optional: also select only the cutters you want to use
3. Open **Window > Toggle System Console** (to monitor progress)
4. **Save your .blend file first!**
5. Click **Multi-Cutter** button

The tool will:
- Use selected cutters, or automatically use all cutters in ``_cutter`` if none are selected
- Cut the mesh into separate objects
- Assign unique names to each tile
- Keep cutter objects available for additional segmentation passes

.. figure:: img/multicutter_result.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Mesh segmented into multiple tiles in Blender outliner]*

**2.4 Clean Floating Geometry**

After segmentation, some tiles may contain unwanted floating fragments:

1. Select a tile
2. Press **Tab** to enter Edit Mode
3. Use **K** (Knife tool) or select and **X > Delete Faces** to remove artifacts
4. Press **Tab** to return to Object Mode
5. Repeat for problematic tiles

.. admonition:: Tip

   Use **Alt+Z** (X-Ray mode) to see through the mesh and identify floating elements more easily.

**2.5 Export Segmented Tiles**

1. Select all tile objects
2. Open **3DSC > Export** panel
3. Set export folder to ``05_RB/03_Model_Library/[YourModelName]/meshpoly/``
4. **Uncheck "Relative Path"** in export settings
5. Click **OBJ Export Batch**
6. Monitor progress in system console

.. figure:: img/export_meshpoly.png
   :width: 600
   :align: center
   
   *[SCREENSHOT: 3DSC export panel with meshpoly folder in EM structure selected]*

.. admonition:: Best Practice

   Save your Blender work file to ``05_RB/02_PROCESSING/blender/`` 
   with a descriptive name like ``[ModelName]_segmentation.blend`` before exporting.
   This preserves your segmentation work for future reference.

Phase 3: High-Resolution Texturing (Metashape + 3DSC Scripts)
--------------------------------------------------------------

**3.1 Prepare Metashape Project**

Create a clean Metashape project for texturing:

1. Open original Metashape project (located in ``05_RB/02_PROCESSING/metashape/``)
2. **File > Save As** with a new name in the same folder:
   
   - Original: ``05_RB/02_PROCESSING/metashape/project.psx``
   - New: ``05_RB/02_PROCESSING/metashape/project_texturing.psx``

3. Optional: Remove unnecessary chunks to simplify
4. Ensure you have:
   
   - Aligned cameras
   - Sparse point cloud
   - NO mesh in the chunk (we'll import tiles)

.. admonition:: EM Structure Locations

   - **Raw photos**: ``05_RB/01_RAW/photos/``
   - **Metashape projects**: ``05_RB/02_PROCESSING/metashape/``
   - **Import tiles from**: ``05_RB/03_Model_Library/[ModelName]/meshpoly/``
   - **Export textures to**: ``05_RB/03_Model_Library/[ModelName]/meshpolytex/``

.. admonition:: Photo Selection Strategy

   For optimal texturing quality:
   
   - Use a **subset of high-quality photos** for texturing
   - Separate "geometry photos" (many, all angles) from "texture photos" (fewer, optimal lighting)
   - Avoid blurred images
   - Ensure consistent lighting

**3.2 Install 3DSC for Metashape Scripts**

1. Download **3DSC for Metashape** from GitHub:
   
   https://github.com/[repository-link]/3DSC-for-Metashape

2. Extract to a known location (e.g., Desktop)
3. The package contains several Python scripts:
   
   - ``import_multiple_models.py`` - Import mesh tiles
   - ``texturize_it.py`` - Automatic texturing
   - ``export_multiple_models.py`` - Export textured results
   - ``rename_chunks.py`` - Utility script

**3.3 Import Mesh Tiles**

1. In Metashape, go to **Tools > Run Script**
2. Select ``import_multiple_models.py``
3. When prompted, select the ``05_RB/03_Model_Library/[ModelName]/meshpoly/`` folder
4. The script will:
   
   - Create one chunk per tile
   - Import each OBJ into its chunk
   - Maintain naming structure

.. figure:: img/metashape_chunks.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Metashape workspace showing multiple chunks, one per tile]*

.. note::

   The script reads all OBJ files from the selected folder. Ensure only the 
   segmented tiles are present in meshpoly/ before running the import.

**3.4 Automatic Texturing**

Now apply high-resolution textures using the texture formula:

1. **Tools > Run Script**
2. Select ``texturize_it.py``
3. The script calculates optimal texture resolution using the formula:

Texture Resolution Formula
~~~~~~~~~~~~~~~~~~~~~~~~~~

For a given tile area and target texel size, the number of textures is calculated as:

.. math::

   N_{\text{tex}} = \frac{(10000 / r_{\text{texel}})^2}{t_{\text{res}}^2 \times ratio}

Where:

- :math:`r_{\text{texel}}` = target resolution in mm/texel (typically 1.2 mm)
- :math:`t_{\text{res}}` = texture resolution in pixels (typically 4096)
- :math:`ratio` = surface coverage ratio (typically 0.6)

**Example Calculation:**

For 100 m² tile with 1.2 mm/texel resolution:

.. math::

   N_{\text{tex}} = \frac{(10000 / 1.2)^2}{4096^2 \times 0.6} \approx 6

Result: **6 textures at 4096×4096 px** per 100 m² tile

.. admonition:: Texture Settings

   The script automatically configures:
   
   - Texture size: 4096×4096 px (adjustable)
   - Mapping mode: Generic
   - Blending mode: Mosaic
   - Enable hole filling
   - Enable ghosting filter

4. Wait for texture generation (can take several minutes per tile)

.. figure:: img/texturing_progress.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Metashape showing textured tile preview]*

**3.5 Export Textured Tiles**

1. **Tools > Run Script**
2. Select ``export_multiple_models.py``
3. Set export folder to ``05_RB/03_Model_Library/[ModelName]/meshpolytex/``
4. If using georeferenced coordinates, provide shift file
5. The script exports:
   
   - OBJ files (mesh geometry)
   - MTL files (material definitions)
   - PNG textures (high-resolution)

.. figure:: img/meshpolytex_folder.png
   :width: 600
   :align: center
   
   *[SCREENSHOT: File explorer showing meshpolytex folder in EM structure with OBJ, MTL, PNG files]*

.. admonition:: Storage Considerations

   The meshpolytex folder can be quite large (500 MB - 2 GB for typical models).
   
   - Store on **NAS** if available (as per EM guidelines for 05_RB)
   - Consider creating a **cloud link** rather than direct sync
   - Keep local copy for active work, archive to NAS when complete


Phase 4: LOD Generation (Blender + 3DSC)
-----------------------------------------

**4.1 Import Textured Tiles**

1. Open new Blender file (or continue from previous)
2. **Import > 3DSC > Import OBJ (Ant File Importer)**
3. Navigate to ``05_RB/03_Model_Library/[ModelName]/meshpolytex/``
4. Import all tiles

.. figure:: img/import_textured.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Blender with fully textured tiled model from EM structure]*

.. tip::

   If working with a very large model, you can import tiles in batches 
   to verify quality before importing the complete set.

**4.2 Verify Quality with Model Inspector**

Use 3DSC's Model Inspector to check texture resolution:

1. Select one or more tiles
2. Open **3DSC > Model Inspector** panel
3. Click **MeanRes** button
4. Review statistics:
   
   - Area (m²)
   - Polygon count
   - Mean resolution (mm/pixel) - should be ~1.2mm
   - Polygons per m² - should be ~1000

5. Click **Export** to save statistics as CSV

.. figure:: img/model_inspector.png
   :width: 600
   :align: center
   
   *[SCREENSHOT: Model Inspector panel showing statistics]*

**4.3 Set LOD0 Base**

Before generating LODs, designate the highest detail level:

1. Select all textured tiles
2. Open **3DSC > LOD Generator** panel
3. Click **LOD 0 (set as)** button

This cleans and renames objects with ``_LOD0`` suffix and proper naming convention (``ob1mt1`` format).

.. admonition:: Naming Convention

   3DSC uses a standardized naming:
   
   - ``ob`` = object
   - ``1`` = object number
   - ``mt`` = material
   - ``1`` = material number
   - ``_LOD0`` = level of detail
   
   This ensures compatibility with game engines like Unreal Engine.

**4.4 Configure LOD Settings**

Set parameters for Level of Detail generation:

1. **Number of LODs**: Typically 2-3 LODs
2. **Padding**: Enable padding ratio (recommended)
3. **Decimation Ratios** (expressed as decimals 0-1):
   
   Example for 3 LODs:
   
   - LOD1: 0.2 (20% of LOD0 = 200 poly/m²)
   - LOD2: 0.04 (20% of LOD1 = 40 poly/m²)
   
   Or:
   
   - LOD1: 0.5 (50% of LOD0 = 500 poly/m²)
   - LOD2: 0.25 (50% of LOD1 = 250 poly/m²)

4. **Texture Resolutions**:
   
   - LOD1: 2048 px
   - LOD2: 512 px
   - LOD3: 128 px (if needed)

5. **Export Folder**: Select where LOD files will be saved

.. figure:: img/lod_settings.png
   :width: 500
   :align: center
   
   *[SCREENSHOT: LOD Generator panel with settings filled]*

**4.5 Generate LODs**

1. Click **Generate** button
2. Monitor progress in system console
3. The tool will:
   
   - Decimate geometry for each LOD
   - Bake textures to lower resolutions
   - Export LOD files to specified folder
   - Create LOD data inside the .blend file

.. admonition:: Processing Time

   LOD generation is time-intensive:
   
   - Small models (~10 tiles): 5-15 minutes
   - Medium models (~50 tiles): 30-60 minutes
   - Large models (100+ tiles): Several hours


Phase 5: Final Reality-Based File
----------------------------------

**5.1 Organize Collections**

After LOD generation, organize your Blender file:

1. Check collection structure:
   
   .. code-block:: text

      RB (Reality Based)
      ├── tile_01_LOD0
      ├── tile_01_LOD1
      ├── tile_01_LOD2
      ├── tile_02_LOD0
      └── ...

2. Clean up any temporary objects
3. Verify all LODs are present

**5.2 Save as RB File**

1. **File > Save As**
2. Navigate to ``05_RB/03_Model_Library/[ModelName]/``
3. Name convention: ``[ModelName]_RB.blend``
   
   Example: ``SeriePola_RB.blend``

4. Final location:
   
   ``05_RB/03_Model_Library/[ModelName]/[ModelName]_RB.blend``

5. This file is now ready for:
   
   - Stratigraphic annotation projects (in ``07_SB/``)
   - Extended Matrix integration (``06_EM/``)
   - PyArchInit workflows
   - Game engine export
   - Dataset publication (``09_Dataset_Publication/``)

.. figure:: img/rb_file_structure.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Final .blend file showing organized LOD structure in EM folder]*

.. admonition:: EM Structure Context

   The complete Model Library subfolder now contains:
   
   .. code-block:: text
   
      05_RB/03_Model_Library/[ModelName]/
      ├── meshmono/              # Decimated canvas
      ├── meshpoly/              # Segmented tiles (untextured)
      ├── meshpolytex/           # Textured tiles
      └── [ModelName]_RB.blend   # ★ Final Reality-Based file
   
   This organization keeps all processing stages together while providing 
   the final, optimized model for downstream use.

**5.3 Use LOD Manager**

To visualize different LOD levels in Blender:

1. Select an object/tile
2. Open **3DSC > LOD Manager** panel
3. Set **LOD Level** (0, 1, or 2)
4. Click **Set LOD** button

The viewport will update to show the selected detail level.

.. figure:: img/lod_manager.png
   :width: 500
   :align: center
   
   *[SCREENSHOT: LOD Manager panel with LOD level selector]*


Phase 6: Integration with Stratigraphic Annotation
---------------------------------------------------

**6.1 Create Extended Matrix Project**

The RB file serves as a base for stratigraphic documentation in the Source-Based models folder:

1. Create new Blender file
2. Save in the EM project structure:
   
   ``07_SB/[ModelName]_EM.blend``
   
   Example: ``07_SB/SeriePola_EM.blend``

3. The complete EM annotation structure:
   
   .. code-block:: text

      06_EM/                           # Extended Matrix data
      ├── [site].graphml              # Stratigraphic relationships
      ├── sources_list.xlsx           # Source documentation
      ├── palette_yed.graphml         # yEd palette for editing
      └── docu_comparativi/           # Comparative documentation folder
      
      07_SB/                           # Source-Based reconstruction
      └── [ModelName]_EM.blend        # ★ Annotation project (this file)

4. **File > Link** (not Import!) the RB file
5. In Link dialog:
   
   - Navigate to: ``05_RB/03_Model_Library/[ModelName]/[ModelName]_RB.blend``
   - Open the .blend file
   - Go to **Collection**
   - Select **RB** collection (contains all LODs)
   - Select **LOD2** collections for initial modeling performance
   - Click **Link**

.. figure:: img/link_rb_file.png
   :width: 700
   :align: center
   
   *[SCREENSHOT: Blender Link dialog showing RB file in EM structure with collections]*

.. important::

   **Link, Don't Import**: Linking keeps the RB file as an external reference. 
   This means:
   
   - Changes to the RB file automatically update in the EM project
   - Multiple EM projects can reference the same RB file
   - The EM file stays lightweight (no duplicate geometry)
   - You can't accidentally modify the reality-based reference data

.. seealso::

   For complete instructions on setting up Extended Matrix projects, 
   refer to the **Extended Matrix User Guide** at: 
   https://extendedmatrix.readthedocs.io

**6.2 Switch LODs for Modeling**

When creating stratigraphic proxies:

1. Select linked RB object
2. Use **3DSC > LOD Manager**
3. Set to **LOD 1** or **LOD 0** for detail work
4. Set to **LOD 2** for overview/performance

**6.3 Proxy Modeling Workflow**

Create stratigraphic unit proxies:

1. Create new collection: ``Proxy``
2. Add geometric primitives (cubes, planes) as needed
3. Model approximate shapes of stratigraphic units (US/USM)
4. Assign colors based on period/phase
5. Link to Extended Matrix graphml data

.. admonition:: Proxy vs Reality-Based

   - **Reality-Based (RB)**: Reference geometry, read-only, high detail
   - **Proxy**: Interpretation layer, editable, simplified volumes

**6.4 Export and Documentation**

The completed annotation project can be exported to:

- **PyArchInit**: SQLite database with 3D linkage
- **Extended Matrix**: GraphML with 3D proxy references
- **XLSX tables**: Spreadsheet documentation
- **Archaeological reports**: Images, metadata, analysis

.. figure:: img/stratigraphic_project.png
   :width: 800
   :align: center
   
   *[SCREENSHOT: Complete EM project with RB model and proxy US overlays]*


Technical Reference
===================

Folder Structure
----------------

This workflow follows the **Extended Matrix (EM) standard folder structure** for archaeological and architectural heritage documentation projects.

.. seealso::

   For complete details on the Extended Matrix folder structure, refer to the 
   **Extended Matrix Documentation** at: https://extendedmatrix.readthedocs.io
   
   Download the EM folder tree template: 
   https://github.com/zalmoxes-laran/ExtendedMatrix/raw/refs/heads/EM_1.5_dev/07_FolderTree/EM_FolderTree_v1.5.zip
   
   For a detailed file-by-file location guide, see :ref:`file_location_appendix`.

EM Project Structure for Digital Replica Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Digital Replica workflow integrates with the EM structure as follows:

.. code-block:: text

   ProjectRoot/
   ├── 00_Quick_Views/                    # Lightweight overview files
   ├── 01_Archival_Sources/               # Previous studies/grey literature
   ├── 02_Published_Sources/              # Historical maps, photos, bibliography
   ├── 03_Documentation/                  # New documentation produced
   ├── 04_Texts/                          # Reports, articles, management docs
   ├── 05_RB/                             # Reality-Based Data ★ MAIN FOLDER FOR THIS WORKFLOW
   │   ├── 01_RAW/                     # Raw sensor data
   │   │   └── photos/                    # ★ Original photogrammetry images
   │   │       ├── IMG_0001.jpg
   │   │       ├── IMG_0002.jpg
   │   │       └── ...
   │   │
   │   ├── 02_PROCESSING/              # Pre/post-processing files
   │   │   ├── metashape/                 # ★ Metashape project files
   │   │   │   ├── project.psx           # Main photogrammetric project
   │   │   │   ├── project_texturing.psx # Texturing project
   │   │   │   └── project.files/        # Associated data
   │   │   │
   │   │   └── blender/                   # Blender work files
   │   │       ├── segmentation.blend    # Intermediate segmentation work
   │   │       └── LOD_generation.blend  # LOD processing file
   │   │
   │   └── 03_Model_Library/           # ★ Processed 3D models (final outputs)
   │       └── [ModelName]/               # One subfolder per model
   │           ├── meshmono/              # ★ Decimated canvas (1000 poly/m²)
   │           │   ├── canvas.obj
   │           │   └── canvas.mtl
   │           │
   │           ├── meshpoly/              # ★ Segmented tiles (untextured)
   │           │   ├── tile_01.obj
   │           │   ├── tile_02.obj
   │           │   └── ...
   │           │
   │           ├── meshpolytex/           # ★ Textured tiles (high-res)
   │           │   ├── tile_01.obj
   │           │   ├── tile_01.mtl
   │           │   ├── tile_01_T_001.png
   │           │   ├── tile_01_T_002.png
   │           │   └── ...
   │           │
   │           └── [ModelName]_RB.blend   # ★ Final Reality-Based file with LODs
   │
   ├── 06_EM/                             # Extended Matrix knowledge graph
   │   ├── [site].graphml                 # Stratigraphic relationships
   │   ├── sources_list.xlsx              # Source documentation
   │   └── palette_yed.graphml            # yEd palette
   │
   ├── 07_SB/                             # Source-Based reconstruction models
   │   └── [ModelName]_EM.blend           # EM annotation project linking RB
   │
   ├── 09_Dataset_Publication/            # Zenodo publication datasets
   └── 10_Presentations/                  # Project presentations

.. admonition:: Key Locations for Digital Replica Workflow

   - **Original photos**: ``05_RB/01_RAW/photos/``
   - **Metashape projects**: ``05_RB/02_PROCESSING/metashape/``
   - **Work Blender files**: ``05_RB/02_PROCESSING/blender/``
   - **All mesh outputs**: ``05_RB/03_Model_Library/[ModelName]/``
   - **Final RB file**: ``05_RB/03_Model_Library/[ModelName]/[ModelName]_RB.blend``
   - **EM annotation project**: ``07_SB/[ModelName]_EM.blend``

Folder Naming Convention
~~~~~~~~~~~~~~~~~~~~~~~~~

When working in teams, the numeric prefixes (05 → 03, etc.) help verbally communicate paths:

- "Put it in zero-five, zero-three" = ``05_RB/03_Model_Library/``
- "Check zero-five, zero-two for the Metashape file" = ``05_RB/02_PROCESSING/``

This system ensures clear communication even over phone or video calls.

File Naming Conventions
-----------------------

- **Canvas**: Single descriptive name (e.g., ``seriepola_canvas.obj``)
- **Tiles**: Sequential numbering (e.g., ``tile_01.obj``, ``tile_02.obj``)
- **Textures**: Format ``[tilename]_T_001.png`` (automatically generated)
- **Blended Files**: 
  
  - Work files: ``[project]_segmentation.blend``
  - RB file: ``[project]_RB.blend``
  - EM file: ``[project]_EM.blend``

Quality Control Checklist
--------------------------

Before finalizing each phase, verify:

**Phase 1 (Canvas)**:

- [ ] Mesh density = 1000 poly/m² (±10%)
- [ ] No holes or non-manifold geometry
- [ ] Clean topology (no flipping faces)
- [ ] Proper scaling (verify in Blender)

**Phase 2 (Segmentation)**:

- [ ] Tile sizes between 60-100 m²
- [ ] No floating fragments
- [ ] Tiles properly aligned at seams
- [ ] All tiles exported successfully

**Phase 3 (Texturing)**:

- [ ] Texture resolution ~1.2 mm/texel
- [ ] No missing textures
- [ ] Minimal color seams between textures
- [ ] PNG format (not JPG) for quality

**Phase 4 (LODs)**:

- [ ] All LOD levels generated
- [ ] Texture quality appropriate per LOD
- [ ] LOD switching works in viewport
- [ ] File size reasonable for target platform

**Phase 5 (RB File)**:

- [ ] Collections properly organized
- [ ] All LODs accessible
- [ ] File saved with descriptive name
- [ ] Backup copy created

Performance Considerations
--------------------------

**Viewport Performance:**

- Work in LOD2 for complex scenes
- Switch to LOD0 only for detail work
- Hide unused tile collections
- Use Blender's Simplify settings

**File Sizes:**

Approximate file sizes for 200 m² model:

- Canvas OBJ: 50-100 MB
- Textured tiles (all): 500 MB - 2 GB
- RB .blend file: 100-500 MB (depends on LODs)
- EM project: 50-200 MB (without RB linked data)

**Hardware Recommendations:**

- Minimum: 16 GB RAM, 4-core CPU, 4 GB VRAM
- Recommended: 32 GB RAM, 8-core CPU, 8 GB VRAM
- For large sites (>500 m²): 64 GB RAM, 16-core CPU, 12 GB VRAM

Troubleshooting
===============

Common Issues and Solutions
---------------------------

**Issue**: Mesh has holes after decimation

**Solution**: 
- Check original dense cloud quality
- Increase photo overlap in problematic areas
- Use Metashape's "Close Holes" tool before decimation

---

**Issue**: Floating geometry fragments after segmentation

**Solution**:
- Enter Edit Mode (Tab)
- Select unwanted fragments
- Delete faces (X > Delete Faces)
- Use knife tool (K) for precise cutting

---

**Issue**: Texture seams visible between tiles

**Solution**:
- Increase texture resolution in problematic areas
- Check photo quality and coverage
- Use Metashape's blending mode "Mosaic" or "Average"
- Apply color correction in post-processing

---

**Issue**: LOD generation fails or crashes

**Solution**:
- Save file before generating LODs
- Reduce number of simultaneous tile processing
- Check available RAM and disk space
- Try generating LODs for tile subsets

---

**Issue**: Georeferenced coordinates cause offset in Blender

**Solution**:
- Use 3DSC shift file import option
- OR work in local coordinates
- Maintain coordinate system consistency across all exports

---

**Issue**: Texture resolution lower than expected (>1.2mm/texel)

**Solution**:
- Verify tile area calculation
- Increase number of textures per tile (modify script)
- Check photo resolution and GSD
- Ensure photos used for texturing are sharp

Best Practices
==============

Photo Acquisition
-----------------

- Maintain consistent overlap (80% front, 60% side)
- Use appropriate GSD for target resolution
- Separate photo sets: geometry (many photos) vs texture (quality photos)
- Avoid blur, ensure proper focus
- Control lighting for texture sets

Project Organization
--------------------

- Use the **Extended Matrix standard folder structure** (EM 1.5)
- Download template: https://github.com/zalmoxes-laran/ExtendedMatrix/raw/refs/heads/EM_1.5_dev/07_FolderTree/EM_FolderTree_v1.5.zip
- Keep raw photos in ``05_RB/01_RAW/photos/``
- Save all Metashape projects in ``05_RB/02_PROCESSING/metashape/``
- Organize outputs in ``05_RB/03_Model_Library/[ModelName]/``
- Use numeric prefixes for verbal communication (e.g., "zero-five, zero-three")
- Name files descriptively and consistently within each folder
- Keep backups at each major phase
- Document coordinate system and units used in project notes
- Prepare datasets for publication in ``09_Dataset_Publication/`` (Zenodo-ready structure)

Workflow Optimization
---------------------

- Process smaller test areas first
- Verify quality at each phase before proceeding
- Use Blender collections to organize complexity
- Leverage LOD system - don't work in LOD0 unnecessarily
- Regular saves and incremental backups

Collaboration
-------------

- Share folder structure template with team
- Use relative paths where possible (except exports)
- Document custom settings and deviations from workflow
- Version control for .graphml and .xlsx files
- Establish naming conventions for entire team

Further Resources
=================

- **3D Survey Collection Documentation**: https://3d-survey-collection.readthedocs.io
- **Extended Matrix**: https://www.extendedmatrix.org
- **Extended Matrix Documentation**: https://extendedmatrix.readthedocs.io
- **Extended Matrix GitHub**: https://github.com/zalmoxes-laran/ExtendedMatrix
- **PyArchInit**: https://pyarchinit.github.io
- **Agisoft Metashape Manual**: https://www.agisoft.com/pdf/metashape-pro_1_8_en.pdf
- **Blender Manual**: https://docs.blender.org

Dataset Publication
-------------------

Once your Digital Replica is complete, you can prepare it for scientific publication:

1. The ``09_Dataset_Publication/`` folder in the EM structure is designed for **Zenodo** publication
2. Each dataset gets:
   
   - Unique DOI (Digital Object Identifier)
   - ZIP archives of model data
   - Standardized Excel metadata files
   - Documentation of processing steps

3. Datasets can reference each other, creating a traceable data chain:
   
   - Example: Link the Digital Replica dataset to the reconstruction model dataset
   - Create collections (e.g., "Basilica Julia Collection")

4. Follow metadata specifications published on Zenodo and in scientific journals

.. seealso::

   For dataset publication guidelines, refer to the 
   **Extended Matrix Documentation** section on Data Publication.

.. admonition:: Support and Community

   For questions and support:
   
   - **3DSC GitHub Issues**: https://github.com/zalmoxes-laran/3D-survey-collection/issues
   - **Extended Matrix Forum**: https://t.me/UserGroupEM
   - **Email**: emanuel.demetrescu at cnr.it

---

*Document version: 1.0 | Last updated: 2025 | Compatible with EM 1.5*
