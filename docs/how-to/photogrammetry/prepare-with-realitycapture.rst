.. _prepare-survey-realitycapture:

================================================
Prepare a digital replica with RealityCapture
================================================

This recipe walks through the bi-directional Blender ↔ RealityCapture
workflow provided by the 3DSC integration module: configuring the tool,
exporting and re-importing models, organizing the LOD hierarchy, and
aligning data from multiple sensors (laser scanner, drone, multiple
camera lenses).

For the parameter catalogue, operator names, and ``.rcbox`` file format
specification, see the tool reference:
:doc:`/reference/tools/realitycapture-tool`.

.. contents:: On this page
   :local:
   :depth: 2

Overview
========

The RealityCapture integration in 3DSC allows users to:

- Export 3D models directly to RealityCapture with configurable quality parameters
- Import OBJ files processed by RealityCapture back into Blender
- Automatically organize imported LOD structures into Blender collections
- Correct naming conventions for mesh, materials, and objects
- Import RealityCapture reconstruction regions (.rcbox files) as 3D geometry
- Manage texturing workflows with precise texel size control

.. figure:: ../../img/RealityCapture_panel_placeholder.png
   :width: 400
   :align: center

   *RealityCapture Integration panel in 3DSC (placeholder)*

.. admonition:: Platform Note

   The RealityCapture Integration panel is **only visible on Windows systems**, as RealityCapture is a Windows-exclusive application.


Installation & Requirements
===========================

**Requirements:**

- Windows 10/11 (64-bit)
- Capturing Reality RealityCapture (any version with CLI support)
- Blender 4.2 or later
- 3DSC Add-on installed and enabled

**Configuration:**

1. Open Blender and navigate to the **3DSC** sidebar panel
2. Expand the **Reality Capture Integration** section
3. Set the **RC Executable Path** to your RealityCapture installation:

   Default: ``C:\Program Files\Capturing Reality\RealityCapture\RealityCapture.exe``

4. Set the **Project Path** to your ``.rcproj`` file
5. Define an **Exchange Folder** for file transfer between applications

.. figure:: ../../img/RealityCapture_settings_placeholder.png
   :width: 400
   :align: center

   *RealityCapture settings configuration (placeholder)*


Complete Workflow Example
==========================

This example demonstrates a typical workflow using both Blender and RealityCapture.

Phase 1: Setup
--------------

1. Open your RealityCapture project with processed photogrammetric data
2. In Blender, configure 3DSC RealityCapture settings:

   - Set RC Executable Path
   - Set Project Path to your .rcproj file
   - Define Exchange Folder

Phase 2: Export from RealityCapture
-----------------------------------

1. In RealityCapture, complete your mesh reconstruction
2. In Blender, use **Export LOD** to export LOD structure
3. RealityCapture generates multi-level detail models to Exchange Folder

Phase 3: Import and Organize in Blender
---------------------------------------

1. Click **Import OBJ** to batch import all models
2. Select all imported objects
3. Run **Correct LOD Names** to standardize naming
4. Run **Organize LODs to Collections** to create LOD hierarchy

.. figure:: ../../img/RealityCapture_workflow_complete_placeholder.png
   :width: 700
   :align: center

   *Complete workflow: RealityCapture to organized Blender collections (placeholder)*


Multi-Sensor Alignment Tutorial
===============================

This section provides detailed guidance on aligning data from multiple sensors (laser scanner, drone, different camera lenses) in RealityCapture. This workflow is particularly useful for complex archaeological or architectural documentation projects.

Overview of Multi-Sensor Approach
---------------------------------

When working with multiple acquisition devices, each sensor produces data with different characteristics. Proper alignment requires careful project organization and parameter tuning.

**Typical Sensor Combinations:**

- Laser Scanner data
- Drone imagery (aerial)
- Ground-based photography (24mm lens)
- Ground-based photography (35mm lens)

Project Structure
-----------------

Create **separate projects** for each sensor combination:

.. list-table::
   :widths: 15 45 40
   :header-rows: 1

   * - Project
     - Content
     - Notes
   * - **1**
     - Laser Scanner + Drone only
     - Export component after alignment
   * - **2**
     - Laser Scanner + 24mm only
     - Export component after alignment
   * - **3**
     - Laser Scanner + 35mm only
     - Export component after alignment
   * - **4**
     - Laser + Drone + 24mm + 35mm
     - Master project - Import and merge

.. figure:: ../../img/RC_multisensor_project_structure_placeholder.png
   :width: 600
   :align: center

   *Multi-sensor project structure in RealityCapture (placeholder)*


Control Points Setup
--------------------

.. admonition:: Important

   Use **Control Points**, NOT Ground Control Points (GCPs), to verify alignment between images and laser data.

**Best Practices:**

- Place control points at features visible in both laser and photographic data
- Use points in common between sensor types to verify alignment quality
- Consider using automatic target detection or scalebars for improved results

.. figure:: ../../img/RC_control_points_placeholder.png
   :width: 500
   :align: center

   *Control points placed between laser and photographic data (placeholder)*


Workflow Phase 1: Individual Sensor Projects (1-3)
--------------------------------------------------

For each single-sensor project (Projects 1, 2, and 3):

1. **Import Data**

   Import laser scanner data and the corresponding image set (drone, 24mm, or 35mm)

2. **Configure Alignment Settings**

   Apply the optimized alignment parameters (see next section)

3. **Run Alignment**

   Execute the alignment process

4. **Place Control Points**

   Add control points at common features between laser and images

5. **Verify Alignment Quality**

   Check that control points show consistent positions

6. **Export Component**

   Use **Workflow > Export Component** to save the aligned dataset

.. figure:: ../../img/RC_export_component_placeholder.png
   :width: 400
   :align: center

   *Export Component menu in RealityCapture (placeholder)*


Workflow Phase 2: Master Project (4)
------------------------------------

In the master project, combine all sensor data:

1. **Import Component**

   Use **Workflow > Import Component** for each exported component (one at a time)

2. **Merge Component**

   When prompted "with images?", select **Yes**

3. **Sensor Lock Option**

   You can choose to **NOT move sensors** during merge. This prevents RealityCapture from forcing alignment and should be disabled in the alignment menu if needed.

4. **Rebuild Sparse Cloud**

   Regenerate the sparse point cloud while keeping sensors fixed (alignment)

5. **Image Usage Options**

   You can disable images from being used for geometry while keeping them aligned for texture purposes

.. figure:: ../../img/RC_merge_component_placeholder.png
   :width: 500
   :align: center

   *Merge Component dialog in RealityCapture (placeholder)*

.. admonition:: Technical Note

   When merging components, RealityCapture may attempt to force alignment between sensors. If you have already verified alignment quality with control points, you can disable automatic sensor movement in the alignment settings.


Alignment Settings Reference
----------------------------

Use these optimized settings for multi-sensor alignment:

.. list-table::
   :widths: 50 25 25
   :header-rows: 1

   * - Parameter
     - Value
     - Notes
   * - **Max feature reprojection error**
     - 3.0 - 4.0
     - **Warning:** 2.0 eliminates too many good tie points!
   * - **Feature detection quality**
     - High
     - Keep default setting
   * - **Max features per mpx**
     - 30,000 - 50,000
     - Higher values improve matching
   * - **Max features per image**
     - 100,000 - 150,000
     - Increase for complex scenes
   * - **Image overlap**
     - High
     - Essential for multi-sensor work
   * - **Image downscale factor**
     - 1
     - Full resolution (optimal)

.. figure:: ../../img/RC_alignment_settings_placeholder.png
   :width: 500
   :align: center

   *Alignment settings panel in RealityCapture (placeholder)*

.. admonition:: Why these values?

   - **Reprojection error 3.0-4.0**: A value of 2.0 is too aggressive and removes valid tie points, especially when matching between different sensor types
   - **High feature counts**: Multi-sensor alignment benefits from more features to find correspondences between different image qualities
   - **No downscaling**: Full resolution ensures maximum feature detection accuracy


Tips for Multi-Sensor Success
-----------------------------

**1. Automatic Target Recognition**

Use coded targets or scalebars that can be automatically detected by RealityCapture. This significantly improves:

- Initial alignment accuracy
- Scale consistency between sensors
- Verification of final results

**2. Selective Geometry Usage**

You can configure images to:

- **Contribute to geometry**: Images are used for mesh reconstruction
- **Texture only**: Images are used only for texturing, not geometry

This is useful when one sensor (e.g., laser) provides better geometry while another (e.g., 24mm photos) provides better texture.

**3. Component Export/Import Strategy**

Export each sensor combination as a separate component. This allows:

- Independent quality verification
- Rollback capability if merge fails
- Modular project management

**4. Alignment Locking**

After achieving good alignment, you can lock sensors to prevent unintended changes during subsequent operations:

- Prevents accidental misalignment during merge
- Maintains verified control point accuracy
- Allows texture-only operations without geometry changes


Troubleshooting
===============

Common Issues and Solutions
---------------------------

**Issue: Panel not visible in Blender**

**Cause:** Running on macOS or Linux

**Solution:** RealityCapture integration requires Windows. Use the CLI interface if cross-platform operation is needed.

**Issue: "RC Executable not found"**

**Cause:** Incorrect path configuration

**Solution:**

- Verify the path to RealityCapture.exe
- Check that RealityCapture is properly installed
- Try running RealityCapture manually to confirm installation

**Issue: Import fails with empty result**

**Cause:** No OBJ files in Exchange Folder

**Solution:**

- Verify files exist in the Exchange Folder
- Check file permissions
- Ensure export from RealityCapture completed successfully

**Issue: LOD organization creates wrong collections**

**Cause:** Non-standard naming in imported files

**Solution:**

- Run **Correct LOD Names** first
- Verify naming pattern matches ``*_LOD#`` format
- Manually rename problematic objects if needed

**Issue: Reconstruction Region imports at wrong location**

**Cause:** Coordinate system mismatch

**Solution:**

- Check the **Apply Shift** option
- Verify the .rcbox file contains correct coordinates
- Compare with known reference points in your scene


.. seealso::

   - :doc:`/reference/tools/realitycapture-tool` — parameters, operators, .rcbox spec
   - :doc:`/how-to/photogrammetry/prepare-with-metashape` — Metashape workflow
   - :doc:`/reference/panels/index` — 3DSC Blender Add-on panels reference
   - :doc:`/reference/tools/tsm` — Texture Smart Mapping system
   - `RealityCapture Documentation <https://support.capturingreality.com/>`_
   - `Extended Matrix Framework <https://www.extendedmatrix.org>`_
   - `3DSC GitHub Repository <https://github.com/zalmoxes-laran/3D-survey-collection>`_
