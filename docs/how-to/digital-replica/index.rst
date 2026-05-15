:orphan:

.. _how-to-digital-replica:

===========================
Digital replica preparation
===========================

End-to-end recipes for preparing a Digital Replica — a multi-LOD,
uniform-density photogrammetric model ready for stratigraphic annotation
and game-engine publication.

The workflow is organised in six phases plus two advisory pages
(best-practices and troubleshooting). Each phase produces the input for the
next; you can also use the phase pages as standalone recipes when only one
step needs revisiting.

For the rationale behind the workflow (why constant polygon density, why
tiled texturing, why a linked Reality-Based file), see
:doc:`/explanation/digital-replica-rationale`.

.. toctree::
   :maxdepth: 1
   :caption: Workflow phases

   phase-1-canvas-creation
   phase-2-segmentation
   phase-3-texturing
   phase-4-lod-generation
   phase-5-rb-file
   phase-6-stratigraphic-integration

.. toctree::
   :maxdepth: 1
   :caption: Advisory

   best-practices
   troubleshooting

Further Resources
=================

- **3D Survey Collection Documentation**: https://3d-survey-collection.readthedocs.io
- **Extended Matrix**: https://www.extendedmatrix.org
- **Extended Matrix Documentation**: https://extendedmatrix.readthedocs.io
- **Extended Matrix GitHub**: https://github.com/zalmoxes-laran/ExtendedMatrix
- **PyArchInit**: https://pyarchinit.github.io
- **Agisoft Metashape Manual**: https://www.agisoft.com/pdf/metashape-pro_1_8_en.pdf
- **Blender Manual**: https://docs.blender.org

Dataset Publication
-------------------

Once your Digital Replica is complete, you can prepare it for scientific
publication:

1. The ``09_Dataset_Publication/`` folder in the EM structure is designed
   for **Zenodo** publication
2. Each dataset gets:

   - Unique DOI (Digital Object Identifier)
   - ZIP archives of model data
   - Standardized Excel metadata files
   - Documentation of processing steps

3. Datasets can reference each other, creating a traceable data chain:

   - Example: Link the Digital Replica dataset to the reconstruction model dataset
   - Create collections (e.g., "Basilica Julia Collection")

4. Follow metadata specifications published on Zenodo and in scientific journals

.. seealso::

   For dataset publication guidelines, refer to the
   **Extended Matrix Documentation** section on Data Publication.

.. admonition:: Support and Community

   For questions and support:

   - **3DSC GitHub Issues**: https://github.com/zalmoxes-laran/3D-survey-collection/issues
   - **Extended Matrix Forum**: https://t.me/UserGroupEM
   - **Email**: emanuel.demetrescu at cnr.it
