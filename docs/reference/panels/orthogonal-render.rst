.. _orthogonal-render:

.. _OrthogonalRender:

Orthogonal Render
=================

The **Orthogonal Render** panel (``VIEW3D_PT_orthogonal_render``) automates
the production of the six standard orthographic views of a mesh — *Front*,
*Back*, *Left*, *Right*, *Top*, *Bottom* — and assembles them into a
print-ready SVG plate (*tavola*) at a true metric scale.

It is the tool used to turn a photogrammetric or laser-scan model of a
single piece (a block, an architectural element, a find) into a documentation
sheet suitable for print or for on-screen zooming.

.. _OrthogonalRenderFIG:

.. figure:: /img/OrthogonalRender_panel.png
   :width: 360
   :align: center

   The Orthogonal Render panel, organised around the three-step workflow.

Source: ``orthogonal_render.py``. Sidebar tab: *3DSC*. Default state:
collapsed (``DEFAULT_CLOSED``).

The panel is organised as a **three-step workflow** — *1 Camera setup* →
*2 Render views* → *3 SVG Layout Export* — followed by three collapsible
sub-panels holding the fine configuration (*Framing & Sizing*,
*Resolution*, *Render Quality & Lighting*). Most projects never need to open
the sub-panels: the defaults are sensible.

At the top the panel shows the active *Object* and the *Output* folder where
the renders and the SVG are written. The ``.blend`` file must be saved before
rendering (the PNGs are written relative to it).

Two options govern how that folder is written:

*Versioning*
   *No versioning* (default) writes straight into the *Output* folder, exactly
   as every earlier release did. *Write into latest version* and *Create new
   version* switch to sibling folders with a numeric suffix —
   ``ortho_renders_v01``, ``_v02``, … — so a re-render never destroys the
   previous set. Only *Create new version* ever makes a new folder, and only
   when you press *Render*; everything that **reads** the renders (the SVG
   export, the panel's own state) always follows the latest existing version,
   so the plate can never end up pointing at an older one. When versioning is
   on, the panel says which folder the next render will land in.

*Don't overwrite existing*
   Skips views whose image file is already on disk and renders only the
   missing ones. This is the way to redo a single view: delete its PNG and
   press *Render 6 Views* again. Off (default) means every render redoes all
   six.

   .. note::

      This is enforced by the tool itself, not by Blender's *Overwrite*
      output setting. That setting is only honoured when rendering an
      animation, and is silently ignored by the single-frame renders this
      tool issues.

.. admonition:: Object name cleaning

   3DSC-managed objects carry typed affixes — a type prefix (``OB_`` objects,
   ``ME_`` meshes) and a Level-of-Detail suffix (``_LOD0`` … ``_LODn``). The
   plate shows the *bare* identifier: an object called ``ME_B1_LOD0`` prints
   as ``B1``. Names without these affixes are shown unchanged. The rendered
   PNG files keep the full object name, so nothing else in the pipeline is
   affected.


Step 1 — Camera setup
---------------------

*Setup Orthogonal Render* (``object.setup_orthogonal_render``)
   Creates (or reuses) the ``OrthoRenderCamera``, an orthographic camera
   framed to the active object's real bounding box, with six keyframed poses
   — one per view. It also builds the three-point *TriLamp* light rig
   parented to the camera (see *Render Quality & Lighting*).

   The camera scale follows the object size times the *Frame Margin*, so
   objects of any size are always fully framed.

.. admonition:: Existing light rig is preserved

   Running *Setup* again does **not** rebuild an existing light rig by
   default, so any manual light adjustment you made is kept. To force a fresh
   rig, tick *Rebuild Light Rig* (see below) before pressing *Setup*.

   The flip side is that a rig inherited from an older scene is preserved
   too, keyframes missing and all — so the scene never repairs itself. When
   that is the case the panel says so under Step 1 and offers *Migrate Light
   Rig*; see *Migrating a rig from an older scene*.


Step 2 — Render views
---------------------

*Render 6 Views* (``render.orthogonal_views``)
   Renders the six orthographic views to the *Output* folder as
   ``<object>_FR.png``, ``_BA``, ``_RI``, ``_LE``, ``_TO``, ``_BO``.

*Render B/W Pass* (``render.orthogonal_views_bw``)
   An **additional** pass, described under *Black & white pass* below.

Right under the buttons the panel shows the settings that decide how long the
render takes — *Engine*, *Samples*, and for Cycles *Device* and *Denoise* —
and they can be changed from there. They are also in the *Render Quality &
Lighting* sub-panel, but that panel is collapsed by default, which is how a
whole afternoon can be rendered on the CPU without anyone noticing. A forced
*CPU*, or a *GPU* with no compute device configured in *Preferences ▸ System*,
is called out in red.

Below that the panel reports the render **resolution** that will be used —
either the object's **size bucket** (*Size: Small (≤ 80 cm) · 2000×2000 px*,
reflecting the live *Size thresholds*) or, in *Drawing scale + DPI* mode, the
scale and DPI it was derived from.

The *Bottom* view is rendered as the true view from below, oriented **N-up
like the Top view** (its left/right are mirrored, as a genuine underside
view). This is handled at the render camera; the templates stay neutral.

.. admonition:: What needs a re-render vs. a re-setup

   Changing *Samples*, *Engine*, *Denoise*, *Device* or a *Resolution* value
   takes effect on the next *Render* — you do **not** need to re-run *Setup*.
   Only the *Frame Margin* (which resizes the camera) requires re-running
   *Setup* + *Render*.


Step 3 — SVG Layout Export
--------------------------

*Create SVG Layout* (``render.create_orthogonal_svg``)
   Composes the six rendered views into an SVG plate using the selected
   template, filling in the title block (object name, dimensions, optional
   logo and location) and drawing the graphic scale bar and the *Scala 1:x*
   caption. Enabled only once the blend is saved and at least one view has
   been rendered.

The scale behaviour is governed by the **Mode**:

*A3 fixed · scale adapts* (``FIXED_SHEET``)
   The sheet is always A3; the **scale adapts** so the piece always fits the
   same paper. Small pieces print at 1:10, larger ones at 1:20, climbing the
   round-scale ladder (1:25, 1:50, 1:100 …) if the piece would overflow the
   box. Because bigger pieces also get more render resolution, the same A3
   can be opened on screen and zoomed while staying sharp. This is the mode
   for a consistent, single-paper archive.

*Scale fixed · sheet adapts* (``FIXED_SCALE``)
   You choose a **fixed drawing scale** once (*Fixed scale*: 1:2, 1:5, 1:10,
   1:20 …); every plate is drawn at that scale and the **paper grows**
   (A2 → A0) to the smallest sheet that fits the piece. The tool warns if the
   piece overflows the largest available sheet. This is the mode when the
   publication requires a constant scale.

*Legacy*
   The original ``MASTER_*`` templates, with no metric-scale processing.

Other fields in this step:

*Fixed scale*
   Only shown in *Scale fixed* mode. The list merges two sources: a baseline
   set (1:1, 1:2, 1:5, 1:10, 1:20, 1:25, 1:50) that is always offered, plus
   every scale for which a ``SCALE_*`` template is installed, so it grows
   automatically as new templates are added (see *Templates and scales*).
   Entries with no matching template say so in their tooltip — the **renders**
   can be produced at that scale, but laying out the plate needs a template.
   This field is also what *Drawing scale + DPI* reads to size the renders.

*Logo*
   Optional image placed in the title block. Leave empty for none (or drop a
   ``logo.png`` into a template folder).

*Location*
   Optional provenance caption printed bottom-left under the silhouette,
   e.g. *Roma, Basilica Iulia*.


Framing & Sizing
----------------

.. _OrthogonalRenderFramingFIG:

.. figure:: /img/OrthogonalRender_framing.png
   :width: 360
   :align: center

   Framing & Sizing sub-panel: frame margin and the size thresholds.

*Frame Margin*
   Padding around the object inside the camera frame (``1.10`` = 10 % air).
   Changing it requires re-running *Setup* + *Render*.

*Size thresholds (meters)* — *Small (≤)*, *Medium (≤)*, *Large (≤)*
   The three cutoffs that sort an object into four buckets. *X-Large* is the
   open bucket above *Large* and is shown read-only (it has no upper bound),
   so all four are visible.

.. admonition:: The *Small* threshold has two jobs

   Besides selecting the *Small* render resolution, the *Small* cutoff is
   also the **1:10 ↔ 1:20 scale boundary** in *A3 fixed* mode: pieces up to
   this size print at 1:10, larger ones at 1:20. The default is ``0.8 m`` —
   the largest piece that fits an A3 box at 1:10.

Changing a threshold takes effect on the next *Render* (Step 2).


Resolution
----------

.. _OrthogonalRenderResolutionFIG:

.. figure:: /img/OrthogonalRender_resolution.png
   :width: 360
   :align: center

   Resolution sub-panel.

*From* chooses how the number of pixels is decided.

**Size buckets** (default) is the historical behaviour: one fixed resolution
per size bucket — *Small* (default 2000²), *Medium* (4000²), *Large* (6000²),
*X-Large* (8000²). There are four resolutions but only three thresholds,
because four buckets need three boundaries (*X-Large* = everything above the
*Large* threshold). The panel also reports what the chosen bucket is worth in
print terms, e.g. *This bucket = 4000 px = ~920 dpi at 1:10*.

**Drawing scale + DPI** derives the resolution from the scale the plate will
actually be drawn at and a *Target DPI*, so the PNG carries exactly the dots
the print needs. This is what removes the manual step of rendering at 1:10 and
doubling the image in Inkscape to obtain 1:5: set the scale to 1:5 and the
renders come out at 1:5.

The scale is not a separate field — it is the scale the plate will use, so it
comes from *Step 3 ▸ Mode*:

* in *Scale fixed · sheet adapts*, it is the *Fixed scale* you chose;
* in *A3 fixed · scale adapts*, it is solved against the A3 box exactly as the
  export solves it, so the two always agree;
* with *Legacy* templates it is assumed to be 1:10.

.. admonition:: Choosing the DPI
   :class: important

   The default is **600 dpi**, not 300. Look at what the size buckets were
   actually delivering: 4000 px across a 1.1 m frame at 1:10 is about
   **920 dpi**, which is precisely why those renders could be enlarged by hand
   afterwards and still hold up. Switching to *Drawing scale + DPI* at 300 dpi
   would be a visible step down from the current plates — 300 dpi at 1:10
   works out to roughly 1300 px per side. Use 300 only when you know the plate
   will be printed once and never enlarged.

The resolution is capped at 16000 px per side. A 1 m block at 1:1 and 600 dpi
would ask for about 31000 px; when the cap bites, the panel says so and
reports the DPI you are actually getting.

Changing a resolution setting takes effect on the next *Render* (Step 2).


Render Quality & Lighting
-------------------------

.. _OrthogonalRenderQualityFIG:

.. figure:: /img/OrthogonalRender_quality.png
   :width: 360
   :align: center

   Render Quality & Lighting sub-panel.

*Engine*
   *Cycles* (default, best quality) or *EEVEE* (much faster, lower fidelity).

*Samples*
   Samples per pixel. Defaults to a low ``20`` for a fast look; raise it if
   the views look noisy — with *Denoise* on, 20 is usually clean enough for
   documentation. See *How many samples* below.

*Denoise*
   Applies denoising (Cycles), letting you use fewer samples.

*Device*
   *Auto* / *GPU* / *CPU*. A warning appears if *GPU* is chosen but no GPU
   compute device is configured in *Preferences ▸ System*. These four settings
   are also shown next to the *Render* button, where they are hard to miss.

*Run benchmark* / *Benchmark Render Speed* (``render.ortho_benchmark``)
   Calibrates a render-time estimate for the current engine/device. Once
   calibrated, the panel shows an estimate for the six views.


How many samples
~~~~~~~~~~~~~~~~

Sampling noise depends on how much of the light arrives indirectly, so the
useful number is not a property of the piece but of the room it was captured
in — and of what surrounds it in the Blender scene.

**Open setting** — the block stands free, nothing bounces light back into it:
the three lamps do nearly all the work and there is little indirect light to
resolve. ``20`` samples with *Denoise* on is normally clean. Raise to ``48``
if the raking side shows speckle in the deepest tool marks.

**Enclosed setting** — the piece sits in a room, a niche, a trench, or is
surrounded by other imported geometry that bounces light: most of what fills
the shadow side is now indirect, which is exactly what converges slowly.
Start at ``128`` and expect to need ``256`` for a light-coloured stone in a
light-coloured room. If it is still noisy at 256, the problem is usually a
large dim emitter rather than the sample count.

Denoising is not a substitute for samples on raking light: it removes noise
by smoothing, and the shallow tool marks a raking key is there to reveal are
exactly what it smooths away first. When the working of the stone is the
point of the plate, prefer more samples over more denoising.


The light rig
~~~~~~~~~~~~~

*Setup* builds a three-point rig — **Key**, **Fill** and **Rim** — parented to
the render camera, in the ``OrthoRender_Lights`` collection. Because the lamps
are parented to the camera they orbit with it, so every view (including the
180°-rolled *Bottom*) is lit from the same image-relative direction.

The rig is described by angles around the subject rather than by raw
positions, and the panel prints them:

.. list-table::
   :header-rows: 1
   :widths: 12 22 22 44

   * - Lamp
     - Incidence
     - Relative power
     - Role
   * - Key
     - ~76°
     - 1.00
     - Raking. Pushed back almost to the subject's own depth so the light
       skims the framed face instead of hitting it head-on; it carves the
       working of the stone and produces most of the shadows.
   * - Fill
     - ~46°
     - 0.20
     - Opposite side, deliberately weak: opens the shadows the key carves
       without flattening them.
   * - Rim
     - ~135°
     - 0.35
     - Genuinely behind the subject, so it detaches the silhouette from the
       transparent background.

**Incidence** is the angle between the lamp and the normal of the face you are
framing: 0° is flat frontal light, 90° is perfectly grazing, above 90° is
behind the subject. This is what "raking" means as a number.

Distances scale with the object size and energies with its square (inverse
square law), so a 2 m block is lit like a 20 cm one.

.. admonition:: What changed in 1.7.0
   :class: important

   The third lamp used to be called *Back* and sat at 79° incidence — beside
   the subject, not behind it, so it was a second side light rather than a rim
   light. It is now called **Rim** and is genuinely behind. The key used to sit
   at 27° incidence, essentially frontal, which is why it produced no raking
   light. And the *Fill* used to be the **brightest** lamp of the three (250 W
   against the key's 150 W), which is the opposite of a three-point rig.

   These are defaults: an existing scene keeps the rig it has until you tick
   *Rebuild Light Rig*.

*Create Light Rig*
   Whether *Setup* builds the rig at all.

*Rebuild Light Rig*
   Shown only when a rig already exists. When on, the next *Setup* rebuilds
   the rig from scratch, resetting positions, energy and keyframes — use it
   only when you want to discard manual light tweaks, or to adopt the new
   default geometry described above.


Editing the lights for a single view
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each lamp is keyframed on all six poses, so a view can be re-lit without
disturbing the other five. Keyframes cover the position, the rotation **and
the intensity** — before 1.7.0 only position and rotation were keyed, so
changing a lamp's power changed it on every view at once.

The procedure:

#. In the timeline, jump to the pose you want to fix. The frames are marked
   ``FR``, ``BA``, ``RI``, ``LE``, ``TO``, ``BO``.
#. Select the lamp — they are in the ``OrthoRender_Lights`` collection — and
   move, rotate or re-power it until that view reads correctly.
#. Press *Key Lights on This View* (``render.ortho_key_lights_here``) in the
   *Render Quality & Lighting* sub-panel. It records position, rotation,
   colour and intensity for **all three** lamps on the current frame only.
#. Press *Render 6 Views*. Only that view changes.

Step 3 can also be done by hand, and this is where a well-known trap lives:
selecting the lamps in the viewport and pressing :kbd:`I` inserts keys for the
**object** transform only. The intensity lives on the light *data*, not on the
object, so it needs a separate key — hover the *Power* field in the light data
properties and press :kbd:`I` there. *Key Lights on This View* does both,
which is the reason it exists.

.. admonition:: "All Channels" does not mean "all frames"
   :class: warning

   In the :kbd:`I` menu, *All Channels* refers to the **transform channels** of
   the selected object — location, rotation and scale together — on the
   **current frame only**. It does not key every frame, and it does not reach
   the light's intensity. Nothing you do in that menu can accidentally
   overwrite the other five views.


Migrating a rig from an older scene
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Migrate Light Rig* (``render.ortho_migrate_light_rig``)
   Adopts a light rig that is already in the file but is not in the shape the
   tool expects.

This is needed for scenes built before 1.7.0, and for scenes whose rig was
appended by hand from a reference ``Luci.blend`` — in both cases the lamps
follow the camera but hold **no keyframes of their own**, so no single view can
be re-lit. *Setup* deliberately leaves an existing rig alone, which means such
a scene never repairs itself: this operator is the way out.

It adopts what is already there **without moving it**. Lamps keep their exact
world pose, their energy and their colour. Only what is missing is added:

* the canonical name (a lamp called ``Back``, or ``OrthoRender_TriLamp-Back``,
  becomes ``OrthoRender_TriLamp-Rim`` — it is *not* duplicated);
* parenting to ``OrthoRenderCamera``, solved so the world pose is unchanged;
* keyframes on the six poses, for the channels that have none. Channels that
  already carry keys are left exactly as they are, so manual work survives.

When the tool detects such a rig it says so at the top of the panel, lists what
is wrong with it, and offers the button there.


Black & white pass
~~~~~~~~~~~~~~~~~~

*Render B/W Pass* (``render.orthogonal_views_bw``)
   Renders an extra set of views tonemapped for reading the working of the
   stone rather than its colour.

It is an **alternative pass, not a change to the setup**: the light rig and all
its keyframes are left exactly as you tuned them. For the duration of the
render the pass borrows the rig — key ×1.6, rim ×1.5, fill ×0.35, applied on
top of whatever each view's keyframes say, so per-view tuning is preserved —
and switches the view transform to *AgX ▸ Greyscale*. Everything is restored
afterwards.

Files are written to a ``bw`` subfolder of the output folder, named
``<object>_<view>_BW.png``, so the colour plate and the B/W plate coexist.
*Don't overwrite existing* applies to this pass too.

.. note::

   The greyscale look keeps the transparent background, so the B/W views drop
   into a plate template like the colour ones. On an unusual OCIO
   configuration where no greyscale look is available, the pass falls back to
   writing 8-bit greyscale files and warns that the transparency is lost.


Templates and scales
---------------------

*Open Templates Folder* (``render.open_templates_folder``)
   Opens the on-disk folder holding the SVG templates so they can be added
   or replaced. 3DSC searches user folders first, then the bundled templates.

Template naming follows ``SCALE_1-<denominator>_<paper>_<capacity>`` for the
fixed-scale family (e.g. ``SCALE_1-10_A2_1m``) and ``FIXED_A3_*`` for the
A3 family. A correctly named ``SCALE_*`` template with the standard
``image_view`` boxes is discovered automatically: the *Fixed scale* menu and
the paper auto-selection pick it up with no configuration.


Typical workflow
----------------

#. Save the ``.blend`` file and select the mesh.
#. Press *Setup Orthogonal Render* (Step 1). If the panel reports a rig from
   an older scene, press *Migrate Light Rig*.
#. Check *Engine*, *Samples* and *Device* in the strip under the *Render*
   button — this is where a render silently ends up on the CPU.
#. Press *Render 6 Views* (Step 2).
#. Look at the six PNGs. If one view is badly lit, jump to its frame, adjust
   the lamps, press *Key Lights on This View*, tick *Don't overwrite
   existing*, delete that one PNG and press *Render 6 Views* again — only
   that view is redone.
#. Optionally press *Render B/W Pass* for a second, tonemapped set.
#. Choose the *Mode* (and, in *Scale fixed*, the *Fixed scale*), set an
   optional *Logo* and *Location*, then press *Create SVG Layout* (Step 3).

.. admonition:: Remember

   In *A3 fixed* mode the scale is chosen for you and printed on the plate;
   in *Scale fixed* mode you set the scale once and the paper grows to fit.
   Both modes always produce a truthful graphic scale bar and *Scala 1:x*
   caption.
