.. _digital-replica-phase-3:

================================================================
Phase 3 — High-Resolution Texturing (Metashape + 3DSC Scripts)
================================================================

This phase applies high-resolution textures to the segmented tiles produced
in :doc:`phase-2-segmentation`. Texturing happens in Agisoft Metashape via
the **3DSC for Metashape** script package, which computes the optimal number
of textures per tile using the Demetrescu-d'Annibale formula
(see :doc:`/explanation/texture-resolution-formula`).

.. contents:: On this page
   :local:
   :depth: 2

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

   For the complete file-by-file location guide, see
   :ref:`file_location_appendix`.

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

.. figure:: /img/metashape_chunks.png
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
3. The script calculates the optimal number of textures per tile using the
   **Demetrescu-d'Annibale texture resolution formula**. For a complete
   derivation and worked examples, see
   :doc:`/explanation/texture-resolution-formula`.

.. admonition:: Texture Settings

   The script automatically configures:

   - Texture size: 4096×4096 px (adjustable)
   - Mapping mode: Generic
   - Blending mode: Mosaic
   - Enable hole filling
   - Enable ghosting filter

4. Wait for texture generation (can take several minutes per tile)

.. figure:: /img/texturing_progress.png
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

.. figure:: /img/meshpolytex_folder.png
   :width: 600
   :align: center

   *[SCREENSHOT: File explorer showing meshpolytex folder in EM structure with OBJ, MTL, PNG files]*

.. admonition:: Storage Considerations

   The meshpolytex folder can be quite large (500 MB - 2 GB for typical models).

   - Store on **NAS** if available (as per EM guidelines for 05_RB)
   - Consider creating a **cloud link** rather than direct sync
   - Keep local copy for active work, archive to NAS when complete

.. seealso::

   - Previous step: :doc:`phase-2-segmentation`
   - Next step: :doc:`phase-4-lod-generation`
   - Formula details: :doc:`/explanation/texture-resolution-formula`
   - Tool reference: :doc:`/reference/tools/metashape-tool`
