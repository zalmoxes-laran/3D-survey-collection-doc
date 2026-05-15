.. _file_location_appendix:

==========================================
File locations — Digital Replica reference
==========================================

This page is the **canonical file-by-file location guide** for the Digital
Replica workflow. It expands the Extended Matrix (EM 1.5) folder structure
with the exact paths used by every Phase of the workflow, plus the file
naming conventions, hardware sizing and performance budget you should plan
against.

This page is referenced from the how-to phase guides, from the
:doc:`/explanation/digital-replica-rationale`, and from the
:doc:`metashape-tool </reference/tools/metashape-tool>` reference whenever a
phrase like "see ``:ref:`file_location_appendix```" appears.

.. contents:: On this page
   :local:
   :depth: 2

Folder Structure
================

This workflow follows the **Extended Matrix (EM) standard folder structure**
for archaeological and architectural heritage documentation projects.

.. seealso::

   For complete details on the Extended Matrix folder structure, refer to
   the **Extended Matrix Documentation** at:
   https://extendedmatrix.readthedocs.io

   Download the EM folder tree template:
   https://github.com/zalmoxes-laran/ExtendedMatrix/raw/refs/heads/EM_1.5_dev/07_FolderTree/EM_FolderTree_v1.5.zip

EM Project Structure for Digital Replica Workflow
-------------------------------------------------

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
------------------------

When working in teams, the numeric prefixes (05 → 03, etc.) help verbally
communicate paths:

- "Put it in zero-five, zero-three" = ``05_RB/03_Model_Library/``
- "Check zero-five, zero-two for the Metashape file" = ``05_RB/02_PROCESSING/``

This system ensures clear communication even over phone or video calls.

File Naming Conventions
=======================

- **Canvas**: Single descriptive name (e.g., ``seriepola_canvas.obj``)
- **Tiles**: Sequential numbering (e.g., ``tile_01.obj``, ``tile_02.obj``)
- **Textures**: Format ``[tilename]_T_001.png`` (automatically generated)
- **Blended Files**:

  - Work files: ``[project]_segmentation.blend``
  - RB file: ``[project]_RB.blend``
  - EM file: ``[project]_EM.blend``

Performance Considerations
==========================

Viewport Performance
--------------------

- Work in LOD2 for complex scenes
- Switch to LOD0 only for detail work
- Hide unused tile collections
- Use Blender's Simplify settings

File Sizes
----------

Approximate file sizes for 200 m² model:

- Canvas OBJ: 50-100 MB
- Textured tiles (all): 500 MB - 2 GB
- RB .blend file: 100-500 MB (depends on LODs)
- EM project: 50-200 MB (without RB linked data)

Hardware Recommendations
------------------------

- Minimum: 16 GB RAM, 4-core CPU, 4 GB VRAM
- Recommended: 32 GB RAM, 8-core CPU, 8 GB VRAM
- For large sites (>500 m²): 64 GB RAM, 16-core CPU, 12 GB VRAM

.. seealso::

   - Workflow how-to entry point: :doc:`/how-to/digital-replica/index`
   - Best practices and QC: :doc:`/how-to/digital-replica/best-practices`
   - Design rationale: :doc:`/explanation/digital-replica-rationale`
