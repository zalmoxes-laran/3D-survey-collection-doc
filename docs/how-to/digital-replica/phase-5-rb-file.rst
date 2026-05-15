.. _digital-replica-phase-5:

==================================
Phase 5 — Final Reality-Based File
==================================

This phase organizes the LOD output from :doc:`phase-4-lod-generation` into
the canonical **Reality-Based (RB) file** — the single ``.blend`` document
that downstream stratigraphic annotation projects, Extended Matrix workflows
and game-engine exports will reference.

.. contents:: On this page
   :local:
   :depth: 2

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

.. figure:: /img/rb_file_structure.png
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
   the final, optimized model for downstream use. For the complete
   file-by-file location guide, see :ref:`file_location_appendix`.

**5.3 Use LOD Manager**

To visualize different LOD levels in Blender:

1. Select an object/tile
2. Open **3DSC > LOD Manager** panel
3. Set **LOD Level** (0, 1, or 2)
4. Click **Set LOD** button

The viewport will update to show the selected detail level.

.. figure:: /img/lod_manager.png
   :width: 500
   :align: center

   *[SCREENSHOT: LOD Manager panel with LOD level selector]*

.. seealso::

   - Previous step: :doc:`phase-4-lod-generation`
   - Next step: :doc:`phase-6-stratigraphic-integration`
   - Tool reference: :doc:`/reference/panels/lod-manager`
