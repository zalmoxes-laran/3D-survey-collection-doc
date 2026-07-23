.. _digital-replica-best-practices:

==============================================
Digital replica — best practices and QC
==============================================

Advisory guidance for high-quality Digital Replicas: photo acquisition,
project organisation, workflow optimisation, team collaboration, and a
per-phase Quality Control checklist that summarises the acceptance criteria
introduced in the :doc:`phase guides <phase-1-canvas-creation>`.

.. contents:: On this page
   :local:
   :depth: 2

Photo Acquisition
=================

- Maintain consistent overlap (80% front, 60% side)
- Use appropriate GSD for target resolution
- Separate photo sets: geometry (many photos) vs texture (quality photos)
- Avoid blur, ensure proper focus
- Control lighting for texture sets

Project Organization
====================

- Use the **Extended Matrix standard folder structure** (EM 1.5)
- Download template: https://github.com/zalmoxes-laran/ExtendedMatrix/raw/refs/heads/EM_1.5_dev/07_FolderTree/EM_FolderTree_v1.5.zip
- Keep raw photos in ``05_RB/01_RAW/photos/``
- Save all Metashape projects in ``05_RB/02_PROCESSING/metashape/``
- Organize outputs in ``05_RB/03_Model_Library/[ModelName]/``
- Use numeric prefixes for verbal communication (e.g., "zero-five, zero-three")
- Name files descriptively and consistently within each folder
- Keep backups at each major phase
- Document coordinate system and units used in project notes
- Prepare datasets for publication in ``09_Dataset_Publication/`` (Zenodo-ready structure)

For the complete file-by-file location guide, see :ref:`file_location_appendix`.

Workflow Optimization
=====================

- Process smaller test areas first
- Verify quality at each phase before proceeding
- Use Blender collections to organize complexity
- Leverage LOD system - don't work in LOD0 unnecessarily
- Regular saves and incremental backups

Collaboration
=============

- Share folder structure template with team
- Use relative paths where possible (except exports)
- Document custom settings and deviations from workflow
- Version control for .graphml and .xlsx files
- Establish naming conventions for entire team

Quality Control Checklist
=========================

Before finalizing each phase, verify:

**Phase 1 (Canvas)** — see :doc:`phase-1-canvas-creation`:

- [ ] Mesh density = 1000 poly/m² (±10%)
- [ ] No holes or non-manifold geometry
- [ ] Clean topology (no flipping faces)
- [ ] Proper scaling (verify in Blender)

**Phase 2 (Segmentation)** — see :doc:`phase-2-segmentation`:

- [ ] Tile sizes between 60-100 m²
- [ ] No floating fragments
- [ ] Tiles properly aligned at seams
- [ ] All tiles exported successfully

**Phase 3 (Texturing)** — see :doc:`phase-3-texturing`:

- [ ] Texture resolution ~1.26 mm²/texel
- [ ] No missing textures
- [ ] Minimal color seams between textures
- [ ] PNG format (not JPG) for quality

**Phase 4 (LODs)** — see :doc:`phase-4-lod-generation`:

- [ ] All LOD levels generated
- [ ] Texture quality appropriate per LOD
- [ ] LOD switching works in viewport
- [ ] File size reasonable for target platform

**Phase 5 (RB File)** — see :doc:`phase-5-rb-file`:

- [ ] Collections properly organized
- [ ] All LODs accessible
- [ ] File saved with descriptive name
- [ ] Backup copy created

.. seealso::

   - Issues: :doc:`troubleshooting`
   - Reference: :doc:`/reference/file-locations`
   - Rationale: :doc:`/explanation/digital-replica-rationale`
