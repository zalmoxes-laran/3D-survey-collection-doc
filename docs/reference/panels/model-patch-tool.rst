.. _model-patch-tool:

.. _3DModelPatchTool:

3D Model Patch Tool
===================

The **3D Model Patch Tool** (panel ``VIEW3D_PT_nonmanifold_filler``) fills
non-manifold areas — typically holes left by photogrammetry or laser
scanning — with new geometry and assigns a *nodata pattern* material
that visually marks the patch as a reconstruction.

This page is the parameter and operator reference for the panel.

Source: ``nonmanifold_filler.py``. Sidebar tab: *3DSC*. Default state:
collapsed (``DEFAULT_CLOSED``).

Parameters
----------

The panel exposes scene properties registered by the module:

``Fill Type``
   Pattern applied to the new faces.

   - ``Solid Color`` — uniform colour (set via ``Color`` swatch).
   - ``Grid Pattern`` — procedural grid driven by ``Axis`` and ``Scale``.

``Color`` (only when ``Fill Type = Solid Color``)
   RGBA colour for the solid fill. Default ``(0.8, 0.8, 0.8, 1.0)``.

``Axis`` (only when ``Fill Type = Grid Pattern``)
   Axis used to orient the grid pattern (``X``, ``Y`` or ``Z``).
   Default ``Y``.

``Scale`` (only when ``Fill Type = Grid Pattern``)
   Grid frequency, range ``[0.1, 20.0]``. Default ``5.0``.

``Use F2 Addon``
   If enabled and the bundled ``F2`` add-on is available, the operator
   delegates the fill step to F2 for cleaner topology. Default ``True``.

``Improve Geometry``
   Beautifies and triangulates the new faces for a smoother patch
   topology. Default ``True``.

Operators
---------

``mesh.fill_nonmanifold`` — *Fill and Apply Pattern*
   Selects non-manifold edges on the active mesh, fills them, and
   assigns the nodata pattern material.

``mesh.adjust_nodata_material`` — *Update Pattern*
   Re-applies the current ``Fill Type`` / ``Color`` / ``Axis`` /
   ``Scale`` values to the existing nodata material without re-filling
   the geometry.

``mesh.remove_nodata_patches`` — *Remove Patches*
   Removes patch faces previously created on the active mesh and clears
   the nodata material assignment.

Typical workflow
----------------

#. Select the mesh that contains holes (must be in Object Mode).
#. Choose a ``Fill Type`` and tune ``Color`` / ``Axis`` / ``Scale``.
#. Press *Fill and Apply Pattern*.
#. Press *Update Pattern* to tweak the visual style without re-filling.
#. Press *Remove Patches* to revert.

.. admonition:: Remember

   The nodata pattern is meant to remain visible in the final
   reconstruction so that interpreters can immediately tell which
   surfaces are *measured* and which are *reconstructed*. Do not bake
   the pattern away.
