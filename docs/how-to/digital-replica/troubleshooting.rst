.. _digital-replica-troubleshooting:

================================================
Digital replica — troubleshooting common issues
================================================

Symptom-driven recipes for the most frequent problems encountered during the
Digital Replica workflow. If an issue is not covered here, consult
:doc:`best-practices` first and then open an issue on the 3DSC GitHub
repository.

.. contents:: On this page
   :local:
   :depth: 2

Common Issues and Solutions
===========================

**Issue**: Mesh has holes after decimation

**Solution**:

- Check original dense cloud quality
- Increase photo overlap in problematic areas
- Use Metashape's "Close Holes" tool before decimation

---

**Issue**: Floating geometry fragments after segmentation

**Solution**:

- Enter Edit Mode (Tab)
- Select unwanted fragments
- Delete faces (X > Delete Faces)
- Use knife tool (K) for precise cutting

---

**Issue**: Texture seams visible between tiles

**Solution**:

- Increase texture resolution in problematic areas
- Check photo quality and coverage
- Use Metashape's blending mode "Mosaic" or "Average"
- Apply color correction in post-processing

---

**Issue**: LOD generation fails or crashes

**Solution**:

- Save file before generating LODs
- Reduce number of simultaneous tile processing
- Check available RAM and disk space
- Try generating LODs for tile subsets

---

**Issue**: Georeferenced coordinates cause offset in Blender

**Solution**:

- Use 3DSC shift file import option
- OR work in local coordinates
- Maintain coordinate system consistency across all exports

---

**Issue**: Texture resolution lower than expected (>1.2mm/texel)

**Solution**:

- Verify tile area calculation (see :doc:`/explanation/texture-resolution-formula`)
- Increase number of textures per tile (modify script)
- Check photo resolution and GSD
- Ensure photos used for texturing are sharp

.. seealso::

   - Advisory: :doc:`best-practices`
   - Formula details: :doc:`/explanation/texture-resolution-formula`
   - Tool reference: :doc:`/reference/tools/metashape-tool`
