.. _circle-from-3-points:

.. _CircleFrom3Points:

Circle from 3 Points
====================

The **Circle from 3 Points** panel (``VIEW3D_PT_circumcenter``) builds a
circle that passes through three selected mesh vertices, using their
circumcenter as the centre. Useful for reconstructing column drums,
apses, well rings, and any radial feature when only a portion of the
arc has been surveyed.

This page is the parameter and operator reference for the panel.

Source: ``utils/circumcenter_tool.py``. Sidebar tab: *3DSC*. Default
state: collapsed (``DEFAULT_CLOSED``). Visible only when the active
object is a mesh.

Required state
--------------

The panel walks the user through three prerequisites and refuses to
expose the operator until all are satisfied:

1. The active mesh must be in **Edit Mode** (the panel offers a
   shortcut button to enter it).
2. Exactly **three vertices** must be selected. The panel reports the
   current selection count and offers a shortcut to switch to vertex
   select mode.
3. The three vertices must not be collinear (validated by the operator
   at execution time).

Parameters
----------

Once the selection is valid, the panel exposes:

``Segments``
   Number of segments used to build the circle mesh. Range ``[3, 128]``,
   default ``32``.

``Circle Color``
   RGBA colour used both for the operator preview and, when
   ``Create as new object`` is enabled, for the resulting object's
   viewport display. Default ``(0.0, 0.8, 1.0, 1.0)`` (cyan).

``Create as new object``
   When enabled (default), the circle is generated as a new object in
   the scene. When disabled, the circle is added to the active object's
   mesh as additional geometry.

Operator
--------

``mesh.apply_circumcenter`` — *Create Circle*
   Reads the three selected vertices, computes the circumcenter and the
   radius, and creates the circle according to the current parameters.

Typical workflow
----------------

#. Select the mesh containing the partial arc.
#. Enter Edit Mode.
#. Switch to *Vertex select* mode.
#. Select exactly three vertices on the surveyed arc.
#. Tune ``Segments`` and ``Circle Color`` if needed.
#. Press *Create Circle*.

.. admonition:: Remember

   The circle is mathematically defined by the three vertices —
   accuracy depends entirely on how well the input points represent the
   intended geometry. Pick vertices spread along the arc (not clustered)
   for a stable fit.
