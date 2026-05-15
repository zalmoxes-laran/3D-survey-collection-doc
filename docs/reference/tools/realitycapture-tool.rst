.. _3DSC4RealityCapture:

============================================
3DSC for RealityCapture — tool reference
============================================

**3DSC for RealityCapture** is an integration module within the 3D Survey
Collection add-on that enables a bi-directional workflow between Blender
and Capturing Reality's RealityCapture software. The module provides
tools for exporting models, managing LOD structures, importing
reconstruction regions, and automating texture generation.

This page is the parameter and operator reference for the tool. For the
workflow-oriented walkthrough (install, complete end-to-end example,
multi-sensor alignment, troubleshooting), see
:doc:`/how-to/photogrammetry/prepare-with-realitycapture`.

.. contents:: On this page
   :local:
   :depth: 2


Parameters Reference
====================

The following parameters control the RealityCapture integration:

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Parameter
     - Default
     - Description
   * - **RC Executable Path**
     - (system default)
     - Path to RealityCapture.exe
   * - **Project Path**
     - (empty)
     - Path to .rcproj project file
   * - **Exchange Folder**
     - (empty)
     - Folder for import/export operations
   * - **Max Resolution**
     - 4096
     - Maximum texture resolution (1024-16384)
   * - **Detail Levels**
     - 5
     - Number of LOD levels to generate (1-10)
   * - **Texel Size**
     - 0.01
     - Target texel size in meters (0.001-1.0)
   * - **Texture Resolution**
     - 2048
     - Texture resolution for export (256-16384)


Tool Reference
==============

Export Tools
------------

**Export to RC**
   Exports the current Blender scene data to RealityCapture with configured parameters.

   **Operator:** ``object.export_rc``

   **Workflow:**

   1. Configure export parameters (Max Resolution, Detail Levels, Texel Size)
   2. Click **Export to RC**
   3. Files are saved to the Exchange Folder
   4. RealityCapture processes the export with specified settings

**Export Cleaned OBJ**
   Exports a cleaned mesh as OBJ to the Exchange Folder.

   **Operator:** ``object.export_cleaned_obj``

   **Output:** ``cleaned.obj`` in Exchange Folder

**Export LOD to Exchange Folder**
   Exports Level of Detail models from RealityCapture.

   **Operator:** ``object.export_lod``

   **Features:**

   - Queries model name from RC project
   - Selects specified model
   - Exports LOD structure to Exchange Folder


Import Tools
------------

**Import OBJ**
   Imports all OBJ files from the Exchange Folder into Blender.

   **Operator:** ``object.import_obj``

   **Features:**

   - Batch import of multiple OBJ files
   - Automatic detection of files in Exchange Folder

**Import Reconstruction Region**
   Imports RealityCapture ``.rcbox`` files as 3D geometry in Blender.

   **Operator:** ``import.reconstruction_region``

   **File Format:** XML-based ReconstructionRegion files

   **Parameters:**

   - **Apply Shift**: When enabled, applies global coordinate shift to the imported geometry

   **Generated Geometry:**

   - Creates a 3D cube representing the reconstruction region
   - Applies correct dimensions (width, height, depth)
   - Sets rotation from yaw/pitch/roll values
   - Optionally applies coordinate transformation

.. figure:: ../../img/RealityCapture_rcbox_import_placeholder.png
   :width: 500
   :align: center

   *Imported reconstruction region as 3D box in Blender (placeholder)*


Texturing Tools
---------------

**Texture in RC**
   Launches the texturing process in RealityCapture with specified parameters.

   **Operator:** ``object.texture_rc``

   **Parameters Applied:**

   - Texel Size: Controls texture detail level
   - Texture Resolution: Maximum texture dimensions

   **RC Commands:** Sets parameters and executes ``-texture all``


LOD Management
--------------

**Organize LODs to Collections**
   Automatically organizes imported LOD objects into Blender collections based on their naming suffix.

   **Operator:** ``organize.lods_to_collections``

   **Pattern Detection:** Identifies ``LOD0``, ``LOD1``, ``LOD2``, etc. suffixes

   **Result:** Creates collections named ``LOD0``, ``LOD1``, ``LOD2`` and moves objects accordingly

.. figure:: ../../img/RealityCapture_lod_collections_placeholder.png
   :width: 400
   :align: center

   *LOD objects organized into collections (placeholder)*

**Correct LOD Names (Mesh & Materials)**
   Standardizes naming conventions for objects, meshes, and materials imported from RealityCapture.

   **Operator:** ``correct.rcnames``

   **Naming Patterns Supported:**

   - Old format: ``base_LODx_number`` converted to ``base_number_LODx``
   - New format: ``base_number_LODx`` (already correct, no change)
   - Generic fallback for unusual cases

   **Scope:**

   - Renames selected objects
   - Updates associated mesh data names
   - Corrects material names

.. admonition:: Best Practice

   Always run **Correct LOD Names** before **Organize LODs to Collections** to ensure proper detection and organization.


ReconstructionRegion File Format
================================

The ``.rcbox`` file is an XML format containing:

.. code-block:: xml

   <ReconstructionRegion>
     <globalCoordinateSystem>...</globalCoordinateSystem>
     <globalCoordinateSystemWkt>...</globalCoordinateSystemWkt>
     <globalCoordinateSystemName>...</globalCoordinateSystemName>
     <isGeoreferenced>true/false</isGeoreferenced>
     <isLatLon>true/false</isLatLon>
     <yawPitchRoll>Y P R</yawPitchRoll>
     <widthHeightDepth>W H D</widthHeightDepth>
     <Header version="X" magic="Y"/>
     <CentreEuclid>X Y Z</CentreEuclid>
     <Residual R="..." t="..." s="..." ownerId="..."/>
   </ReconstructionRegion>

**Key Elements:**

- **yawPitchRoll**: Rotation angles for the region box
- **widthHeightDepth**: Dimensions of the reconstruction volume
- **CentreEuclid**: Center coordinates in Euclidean space
- **isGeoreferenced**: Indicates if coordinates are georeferenced


Credits and License
===================

**Author:**
  Emanuel Demetrescu
  CNR-ISPC (Consiglio Nazionale delle Ricerche - Istituto di Scienze del Patrimonio Culturale)
  Rome, Italy

**License:**
  GNU General Public License v3 (GPL-3)

**Part of:**
  Extended Matrix Framework
  https://www.extendedmatrix.org


.. seealso::

   - :doc:`/how-to/photogrammetry/prepare-with-realitycapture` — workflow walkthrough
   - :doc:`/reference/tools/metashape-tool` — Metashape integration tools
   - :doc:`/reference/panels/index` — 3DSC Blender Add-on panels reference
   - :doc:`/reference/tools/tsm` — Texture Smart Mapping system
   - `RealityCapture Documentation <https://support.capturingreality.com/>`_
   - `Extended Matrix Framework <https://www.extendedmatrix.org>`_
   - `3DSC GitHub Repository <https://github.com/zalmoxes-laran/3D-survey-collection>`_
