.. _rotation-constrained:

.. _RotationConstrained:

Rotation Constrained
====================

The **Rotation Constrained** panel (``VIEW3D_PT_rotation_constrained``)
performs a controlled bend on selected mesh faces by rotating them
around one axis while constraining the vertex motion along another.
It is the preferred tool for hinging panels, opening *swing-out*
elevations, or modelling the rotation of a fragment around a known
pivot edge.

This page is the parameter and operator reference for the panel.

Source: ``utils/rotation_constrained.py``. Sidebar tab: *3DSC*. Default
state: collapsed (``DEFAULT_CLOSED``). Visible only when the active
object is a mesh.

Required state
--------------

The panel walks the user through two prerequisites before exposing the
operator:

1. The mesh must be in **Edit Mode** (the panel offers a shortcut
   button to enter it).
2. At least **one face must be selected** (the panel offers a shortcut
   to switch to face select mode).

Parameters
----------

``Rotation Axis`` (``rc_raxis``)
   Pivot axis for the rotation (``X``, ``Y`` or ``Z``).

``Constraint Axis`` (``rc_caxis``)
   Axis along which the moved vertices are allowed to travel. **Must be
   different from** ``Rotation Axis`` — if equal, the panel shows a
   warning and the operator refuses to run.

``Rotation Point`` (``rc_rpoint``)
   Pivot anchor used for the rotation (typically the median of the
   selected edge — refer to source for the supported enum values).

``Mirror`` (``rc_rmirror``)
   When enabled, mirrors the rotation around the chosen pivot to produce
   symmetrical bends.

``Degrees`` (``rc_rdeg``)
   Rotation amount in degrees. A value of ``0`` is treated as a no-op
   and reported as such.

Operators
---------

``mesh.apply_rotation_constrained`` — *Apply Rotation*
   Validates the selection and the axis configuration, then calls
   ``mesh.rotation_constrained`` with the panel parameters.

``mesh.rotation_constrained``
   The underlying low-level operator. Can be invoked directly or via
   the ``Alt + Shift + R`` keyboard shortcut documented in the panel.

Typical workflow
----------------

#. Enter Edit Mode on the target mesh.
#. Select one or more faces representing the moving panel.
#. Pick ``Rotation Axis`` (the hinge) and ``Constraint Axis`` (the
   direction the free edge is allowed to travel along).
#. Set ``Rotation Point`` and ``Degrees``; toggle ``Mirror`` if needed.
#. Press *Apply Rotation*, or use ``Alt + Shift + R``.

.. admonition:: Remember

   ``Rotation Axis`` and ``Constraint Axis`` must always be different —
   otherwise the rotation is geometrically undefined. The panel
   surfaces this with an inline warning, but no movement happens until
   the configuration is valid.
