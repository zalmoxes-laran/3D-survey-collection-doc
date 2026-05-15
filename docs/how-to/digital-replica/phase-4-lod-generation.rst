.. _digital-replica-phase-4:

=========================================
Phase 4 — LOD Generation (Blender + 3DSC)
=========================================

This phase generates multiple Levels of Detail (LODs) from the textured tiles
produced in :doc:`phase-3-texturing`. The 3DSC **LOD Generator** decimates
geometry and bakes lower-resolution textures so the final Reality-Based file
can be efficiently visualized at different zoom levels.

.. contents:: On this page
   :local:
   :depth: 2

**4.1 Import Textured Tiles**

1. Open new Blender file (or continue from previous)
2. **Import > 3DSC > Import OBJ (Ant File Importer)**
3. Navigate to ``05_RB/03_Model_Library/[ModelName]/meshpolytex/``
4. Import all tiles

.. figure:: /img/import_textured.png
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

.. figure:: /img/model_inspector.png
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

.. figure:: /img/lod_settings.png
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

.. seealso::

   - Previous step: :doc:`phase-3-texturing`
   - Next step: :doc:`phase-5-rb-file`
   - Tool reference: :doc:`/reference/panels/lod-generator`
