.. _digital-replica-phase-6:

====================================================
Phase 6 — Integration with Stratigraphic Annotation
====================================================

This final phase shows how to integrate the Reality-Based file produced in
:doc:`phase-5-rb-file` into a stratigraphic annotation project, including
Extended Matrix proxy modelling and downstream documentation exports.

.. contents:: On this page
   :local:
   :depth: 2

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

.. figure:: /img/link_rb_file.png
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

.. figure:: /img/stratigraphic_project.png
   :width: 800
   :align: center

   *[SCREENSHOT: Complete EM project with RB model and proxy US overlays]*

.. seealso::

   - Previous step: :doc:`phase-5-rb-file`
   - Advisory: :doc:`best-practices`
   - Issues: :doc:`troubleshooting`
