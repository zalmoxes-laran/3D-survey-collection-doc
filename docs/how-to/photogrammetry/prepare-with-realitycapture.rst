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


.. _realityscan-tileset-3tz:

Export a Cesium tileset and pack it as .3tz
===========================================

RealityScan (the new name of RealityCapture) exports a model as **Cesium 3D
Tiles**: a tileset that a viewer loads piece by piece, the coarse levels from
far away and the fine ones as the camera comes closer. This section shows the
export settings to use and how to turn the result into one ``.3tz`` file with
3DSC.

Why one ``.3tz`` file
---------------------

RealityScan writes a ``.json`` file beside a folder with the same name, and
the folder holds thousands of tiles. A ``.3tz`` is the same tileset in one
file:

- it travels as one file (a copy, an upload, a deposit) and nothing gets
  lost on the way;
- a viewer reads it piece by piece, without unpacking it;
- the same folder always gives the same bytes, so the file's fingerprint
  (sha256) names its content, and 3DSC writes a stamp beside it that says
  where it comes from.

EMStudio, Heriverse and the EM tools read the ``.3tz`` directly.

Step 1 · Export from RealityScan
--------------------------------

The example is the **Basilica Iulia** in the Roman Forum: a model made of
laser scans (TLS) and drone photographs (UAV), in the coordinate system
**EPSG:6708** (RDN2008 / UTM zone 33N), the one of the Basilica's
reconstruction files. Replace the CRS and the checks with those of your site.

1 · Before the export: the coordinate system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The export dialog has no coordinate system: the tileset is written in the
**output coordinate system of the project**. Set it first, in the project's
settings (*coordinate systems*):

- **Project coordinate system**: EPSG:6708.
- **Output coordinate system**: EPSG:6708.

Then check that the model is really there: in the 3D view read the
coordinates of a point you know. The Basilica sits around **E 291 300,
N 4 640 880** (metres). If you read small numbers (tens or hundreds of
metres), the model is in a local frame: export it like this and the tileset
lands at the equator. A useful check is a benchmark of the survey (for the
Basilica, benchmark 49): its height in the model must be its height in the
survey.

.. warning::

   The laser scans must be registered in the same system as the rest of the
   documentation. In October 2026 a TLS export of the Basilica was correct
   inside RealityScan but rotated by 6.6° and shifted by about 110 m and 16 m
   in height against the reconstruction files: the scans had been registered
   in another frame. No export setting fixes that; the registration does.

2 · Open the export
~~~~~~~~~~~~~~~~~~~

Select the textured model, then *SCENE 3D ▸ TOOLS ▸ Export ▸ Level of Detail*
and choose the type **Cesium 3D Tiles (\*.json)**. Give the file a short name
without spaces, for example ``Basilica_TLS_UAV``. RealityScan may warn that
the feature is experimental: press OK.

.. figure:: ../../img/realityscan_export_tiles_placeholder.png
   :width: 500
   :align: center

   *The Level of Detail dialog for Cesium 3D Tiles (placeholder)*

3 · The parameters, one by one
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 24 22 54

   * - Parameter
     - Use
     - Why
   * - **Initial simplification** · Type
     - **None**
     - It sets the finest level of the tileset. *None* keeps every triangle
       of the model: the finest tiles are the model itself. Use *Relative*
       or *Absolute* only for a light copy, never for the reference tileset.
   * - **Iterative simplification** · Type
     - **Relative**, 50 %
     - The step from one level to the next coarser one (the only type
       allowed is *Relative*). With 50 % every level has half the triangles
       of the one below: few levels, and each one lighter by the same
       ratio.
   * - **Export textures**
     - **On**
     - Without it the tileset is grey geometry. The model must already be
       textured.
   * - **Source Layer**
     - the texture layer of the final texturing
     - If the project has more than one texture layer (a test, a colour
       correction), choose the one you consider final.
   * - **Texel size**
     - **2 × Optimal**
     - The best texture quality written in the tileset: a smaller texel means
       sharper and heavier. *Optimal* is the texel of the photographs. On the
       Basilica it produced textures of 8192 × 8192 pixels for every tile,
       about 300 MB each on the graphics card: four tiles fill a laptop.
       Twice the optimal value keeps the detail you see on screen and divides
       the weight by four.
   * - **Texture Format**
     - **.jpg**
     - Read by every viewer and light. *.png* is lossless but several times
       heavier; *.webp* is not read by every viewer.
   * - **Maximum node triangle count**
     - **20 000 – 30 000**
     - How many triangles a tile holds before it is split. On the Basilica,
       10 000 gave many small tiles (many requests, the viewer always busy);
       100 000 gave few huge tiles, with tiny error values, and the viewer
       stayed on the coarsest level. 20 000 – 30 000 is the middle way.
   * - **Bandwidth Scale**
     - **1**
     - Below 1 the viewer streams faster and shows less detail, above 1 the
       opposite. Leave it at 1: the balance between quality and speed is
       tuned later in the viewer (EMStudio), for each device, without
       exporting again.
   * - **Altitude**
     - the model's own heights
     - Keep the heights of the project. *Clamp to WGS84 ellipsoid* moves the
       model onto the ellipsoid, metres away from its real height.
   * - **Compression**
     - **No**
     - Compressed tiles must be unpacked at every load, and some viewers
       cannot do it inside a ``.3tz``. Disk space is not the problem here.

Press OK. RealityScan writes, in the chosen folder:

- ``Basilica_TLS_UAV.json``, the root of the tileset;
- ``Basilica_TLS_UAV/``, the folder of the tiles (thousands of files).

The two travel together: the ``.json`` alone is empty, the folder alone has no
root. Step 2 turns them into one file.

Step 2 · Pack the tileset into a .3tz with 3DSC
-----------------------------------------------

You need 3DSC **1.7.0-dev.72 or later**: in Blender, *Edit ▸ Preferences ▸ Get
Extensions*, update *3D Survey Collection*. The version is written at the top
of the 3DSC panels.

#. In the 3D Viewport sidebar open **3DSC ▸ Cesium 3D Tiles**.
#. Press **Pack a tileset into .3tz**.
#. In the file browser choose **the folder that holds the export** (the
   ``.json`` and the folder of the same name), or the folder of the tiles
   itself. Keep *Verify after writing* on.
#. Press **Accept**.

3DSC writes ``<name>.3tz`` beside the export (``Basilica_TLS_UAV.3tz``), checks it against the original
tiles, and writes the stamp ``<name>.3tz.stamp.json`` beside it. The original
export is only read. The log of the panel says how many files went in, the
size, the time and the fingerprint.

The same button packs any folder with ``tileset.json`` at its root (Metashape,
3DSC's own export, other generators). If the chosen folder holds more than one
RealityScan export, 3DSC asks you to choose the folder of one of them.

.. note::

   EMStudio packs the same file, byte for byte: drop the export on the Viewer
   and press **Prepare the package (.3tz)**, see `Load models and tilesets
   <https://docs.extendedmatrix.org/projects/emstudio-doc/en/1.6/how-to/space/load-models-and-tilesets.html>`_.
   That road starts from an open study (an ``em.json``): use it when the
   tileset goes into a study right away.


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
