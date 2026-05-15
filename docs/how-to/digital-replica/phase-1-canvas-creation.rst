.. _digital-replica-phase-1:

=======================================================
Phase 1 — High-Resolution Mesh Preparation (Metashape)
=======================================================

This phase creates the **canvas** — a decimated, uniform-density mesh that
serves as the base geometry for the Digital Replica. The canvas is exported
from Agisoft Metashape and stored in the EM ``05_RB/03_Model_Library/``
structure for the next phases.

.. contents:: On this page
   :local:
   :depth: 2

**1.1 Photo Alignment and Mesh Generation**

Start with a standard photogrammetric project in Agisoft Metashape:

1. Align photos using standard workflow
2. Build dense cloud
3. Generate high-resolution mesh

.. figure:: /img/metashape_higres_mesh.png
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

.. figure:: /img/decimated_canvas.png
   :width: 800
   :align: center

   *[SCREENSHOT: Decimated mesh at 1000 poly/m² showing uniform density]*

.. admonition:: Why 1000 polygons/m²?

   This density provides an optimal balance:

   - Sufficient detail to recognize most features
   - Low enough for efficient editing in Blender
   - Compatible with game engines (Unreal, Unity, Godot, O3DE)
   - Avoids flipping geometry artifacts common in very dense meshes

   For the full rationale behind this choice, see
   :doc:`/explanation/digital-replica-rationale`.

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
   and separate from raw data and processing files. For the complete
   file-by-file location guide, see :ref:`file_location_appendix`.

.. figure:: /img/export_meshmono.png
   :width: 600
   :align: center

   *[SCREENSHOT: Metashape export dialog with OBJ settings]*

.. seealso::

   - Next step: :doc:`phase-2-segmentation`
   - Tool reference: :doc:`/reference/tools/metashape-tool`
