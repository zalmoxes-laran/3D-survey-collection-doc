.. _digital-replica-phase-2:

============================================
Phase 2 — Mesh Segmentation (Blender + 3DSC)
============================================

This phase divides the canvas exported in :doc:`phase-1-canvas-creation` into
manageable tiles using the **LOD Cutter** tool inside Blender. The output is
a set of segmented OBJs ready for high-resolution texturing.

.. contents:: On this page
   :local:
   :depth: 2

**2.1 Import Canvas in Blender**

1. Open Blender
2. Install 3D Survey Collection add-on if not already installed
3. **Import > 3DSC > Import OBJ (Ant File Importer)**
4. Navigate to ``05_RB/03_Model_Library/[YourModelName]/meshmono/``
5. Select the OBJ file

.. figure:: /img/blender_import_3dsc.png
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

.. figure:: /img/lod_cutter_grid.png
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

.. figure:: /img/multicutter_result.png
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

.. figure:: /img/export_meshpoly.png
   :width: 600
   :align: center

   *[SCREENSHOT: 3DSC export panel with meshpoly folder in EM structure selected]*

.. admonition:: Best Practice

   Save your Blender work file to ``05_RB/02_PROCESSING/blender/``
   with a descriptive name like ``[ModelName]_segmentation.blend`` before exporting.
   This preserves your segmentation work for future reference.

.. seealso::

   - Previous step: :doc:`phase-1-canvas-creation`
   - Next step: :doc:`phase-3-texturing`
   - Tool reference: :doc:`/reference/panels/segmentation`
