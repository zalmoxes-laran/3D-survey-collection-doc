.. _orthogonal-render:

.. _OrthogonalRender:

Orthogonal Render
=================

The **Orthogonal Render** panel (``VIEW3D_PT_orthogonal_render``)
automates the production of six orthographic views (Front, Back, Left,
Right, Top, Bottom) of a selected mesh, with resolution rules driven by
the object's real-world size, and assembles the renders into a printable
SVG sheet template.

This page is the parameter and operator reference for the panel.

Source: ``orthogonal_render.py``. Sidebar tab: *3DSC*. Default state:
collapsed (``DEFAULT_CLOSED``).

Size categories
---------------

Objects are bucketed by their longest dimension. Each bucket has a
configurable cutoff (in metres) and a target render resolution (in
pixels).

``Small (≤)`` / ``Small`` resolution
   Default cutoff ``0.5 m``. Default resolution: configured per project.

``Medium (≤)`` / ``Medium`` resolution
   Default cutoff ``1.0 m``.

``Large (≤)`` / ``Large`` resolution
   Default cutoff ``2.0 m``.

``X-Large`` resolution
   Used when the object's longest dimension exceeds ``Large``.

The four resolution scene properties registered are
``ortho_render_small_resolution``, ``..._medium_...``,
``..._large_...``, ``..._xlarge_...``.

Output settings
---------------

``Output``
   Folder where the six PNG renders and the final SVG are saved. The
   panel refuses to render until the ``.blend`` file has been saved
   (PNGs are written next to the blend).

SVG layout
----------

``Template``
   Selects the SVG template family used to compose the printable sheet.
   Two families are supported in code (``FIXED_SHEET`` and
   ``FIXED_SCALE``); the panel exposes them via
   ``scene.ortho_template_family``.

   - ``FIXED_SHEET`` — renders at the resolution required to fill the
     sheet at a virtual 1:10 zoom level.
   - ``FIXED_SCALE`` — renders at the resolution required to print at
     the declared scale and DPI.

Operators
---------

``object.setup_orthogonal_render`` — *Setup*
   Creates the ``OrthoRenderCamera`` and lighting rig sized to the
   active object's bounding box.

``render.orthogonal_views`` — *Render*
   Renders all six orthographic views to the chosen output folder.

``render.create_orthogonal_svg`` — *Create SVG*
   Composes the rendered views into an SVG sheet using the selected
   template. Enabled only when the template is installed, the blend is
   saved, and at least one render is present.

``render.open_templates_folder`` — *Open Templates Folder*
   Opens the on-disk folder containing the SVG templates so they can be
   added or replaced.

Typical workflow
----------------

#. Save the ``.blend`` file.
#. Select the mesh to render.
#. Adjust ``Size`` cutoffs and ``Resolution`` settings if needed.
#. Press *Setup* — this creates the camera rig.
#. Press *Render* — six PNGs are produced.
#. Choose a ``Template`` and press *Create SVG*.

.. admonition:: Remember

   Resolutions are independent per size bucket. Tune them once per
   project so that small artefacts and large monuments share a coherent
   visual scale across the report.
