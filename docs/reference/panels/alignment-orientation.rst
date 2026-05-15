.. _alignment-orientation:

.. _AlignmentOrientation:

Alignment Orientation
=====================

The **Alignment Orientation** panel (``VIEW3D_PT_alignment_orientation``)
creates a custom Blender transform orientation from two points recorded
with the 3D cursor. It is the recommended way to derive a working axis
system from survey markers (e.g. wall corners, total-station prisms,
photogrammetric targets) without manually entering Euler angles.

This page is the parameter and operator reference for the panel.

Source: ``utils/alignment_orientation_tool.py``. Sidebar tab: *3DSC*.
Default state: collapsed (``DEFAULT_CLOSED``).

Workflow inputs
---------------

The panel stores two points as scene properties:

``alignment_point_1`` (*Point 1*)
   First reference point. Captured from the current 3D cursor position
   when *Record* is pressed.

``alignment_point_2`` (*Point 2*)
   Second reference point. Captured the same way.

Both points are displayed in the panel as ``(x, y, z)`` formatted to two
decimals once recorded.

Orientation parameters
----------------------

Only visible after both points have been recorded.

``Name``
   Name assigned to the custom transform orientation and to the
   optional reference empty object. Default ``D.x.x_alignment`` (follows
   the Extended Matrix naming convention for stratigraphic alignments).

``Type`` — alignment strategy
   - ``XYZ from Points`` — Point 1 → Point 2 defines the X axis; Y is
     orthogonal in the horizontal plane; Z is derived assuming X and Y
     are on the same level.
   - ``XY axis from Points - Z not modified`` — Point 1 is the origin,
     Point 2 defines the X direction, Z remains the global Z axis.
     (Default — the safer choice when the survey is approximately
     level.)

``Keep Object``
   When enabled (default), the empty used to anchor the orientation is
   left in the scene so it can be re-used or re-named later. When
   disabled, the empty is created only as a scratchpad and removed at
   the end.

Operators
---------

``view3d.record_cursor_location`` — *Record*
   Stores the current 3D cursor location into the scene property
   referenced by ``location_prop`` (either ``alignment_point_1`` or
   ``alignment_point_2``).

``view3d.clear_alignment_points`` — *Clear*
   Resets both recorded points to ``(0, 0, 0)``.

``view3d.create_alignment_orientation`` — *Create Orientation*
   Creates the named custom transform orientation (visible in the
   Blender header *Transformation Orientations* dropdown) and the
   optional reference object.

Typical workflow
----------------

#. Position the 3D cursor on the first reference target (Shift + Right
   click or Snap → Cursor to Selected).
#. Press *Record* next to ``Point 1``.
#. Move the cursor to the second target and press *Record* next to
   ``Point 2``.
#. Choose ``Type`` and confirm ``Name``.
#. Press *Create Orientation*. The new orientation is now selectable in
   the Blender transform header.

.. admonition:: Remember

   The created orientation is a standard Blender custom orientation —
   it persists with the blend file and can be applied to any subsequent
   transform operation.
