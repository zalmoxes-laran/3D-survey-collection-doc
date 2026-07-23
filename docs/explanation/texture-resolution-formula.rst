.. _texture-resolution-formula:

==========================================
Texture resolution formula
==========================================

The **Demetrescu-d'Annibale texture resolution formula** is the algorithm
3DSC uses to compute how many 4096 px texture atlases are needed to texture a
segmented photogrammetric tile at a fixed, homogeneous ground resolution. It
is the single source of truth for every place in the documentation that quotes
the formula — the Metashape tool reference and the
:doc:`Digital Replica Phase 3 how-to </how-to/digital-replica/phase-3-texturing>`
both link back here.

The formula was published as **Equation (1)** in
`Demetrescu et al. 2026 <https://doi.org/10.3390/rs18020203>`__
(*Remote Sensing* 18(2):203, open access, CC-BY) and is implemented in the
:doc:`3DSC for Metashape </reference/tools/metashape-tool>` add-on
(Supplementary Code S1 of that article).

.. contents:: On this page
   :local:
   :depth: 2

The formula
===========

For a tile of surface area :math:`A_{\text{tile}}`, the number of texture
atlases required to hold the target texel density is:

.. math::

   n_{\text{tex}} = \operatorname{round}\!\left(
     \frac{A_{\text{tile}}}{100} \times
     \frac{(L_{\text{ref}} / r_{\text{target}})^2}{s_{\text{tex}}^2 \times r_{\text{uv}}}
   \right), \qquad n_{\text{tex}} \geq 1

Where:

- :math:`n_{\text{tex}}` = number of :math:`4096^2` texture atlases required
  (minimum 1)
- :math:`A_{\text{tile}}` = actual surface area of the tile in m²
  (from ``chunk.model.area()`` in Metashape)
- :math:`L_{\text{ref}}` = **10 000 mm** — side length of the reference
  100 m² square (10 m × 10 m)
- :math:`r_{\text{target}}` = **1.26 mm²/texel** — empirically determined
  target texture density
- :math:`s_{\text{tex}}` = **4096 px** — texture atlas dimension
- :math:`r_{\text{uv}}` = **0.6** — UV-space utilization efficiency
  (photogrammetric UV atlasing leaves ~40 % of texture space unused)
- :math:`\operatorname{round}(\cdot)` = standard rounding (0.5 rounds up)

The formula operates in **two conceptual steps**.

Step 1 — Reference calculation
------------------------------

How many atlases a standard 100 m² tile needs:

.. math::

   n_{\text{ref}} = \frac{(10000\ \text{mm} / 1.26\ \text{mm}^2/\text{texel})^2}
   {4096^2 \times 0.6} \approx 6.26 \text{ textures per } 100\ \text{m}^2

Step 2 — Area scaling
---------------------

Scale that reference proportionally by the actual tile area:

.. math::

   n_{\text{tex}} = \operatorname{round}\!\left( n_{\text{ref}} \times
   \frac{A_{\text{tile}}}{100} \right)

Worked example
==============

A tile of :math:`A_{\text{tile}} = 50\ \text{m}^2` needs
:math:`6.26 \times (50/100) = 3.13 \rightarrow 3` textures. A 55 m² tile gives
:math:`6.26 \times 0.55 = 3.44 \rightarrow 3`; a 60 m² tile gives
:math:`6.26 \times 0.60 = 3.76 \rightarrow 4`.

Using standard rounding (rather than always rounding up) optimizes texture
memory: tiles slightly above a threshold receive an extra atlas, while those
slightly below keep the lower count.

Reference table
===============

Texture count per tile area, as published (Table 3 of Demetrescu et al. 2026),
at 1.26 mm²/texel, 4096 px atlases, :math:`r_{\text{uv}} = 0.6`:

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Tile area (m²)
     - Textures (4096 px)
   * - 0 – 16
     - 1
   * - 16 – 33
     - 2
   * - 33 – 49
     - 3
   * - 49 – 66
     - 4
   * - 66 – 83
     - 5
   * - 83 – 100
     - 6

.. note::

   The published tiling standard caps the **standard tile at 100 m²** (6
   atlases). The Metashape add-on additionally offers a *Texturize Models
   (200 m² limit)* mode that extends this to larger tiles and caps at 12
   atlases; this is a tool convenience beyond the published standard, intended
   for oversized architectural features rather than the normal tile size.

Reference implementation
========================

The formula is implemented in ``3DSC_MS_GUI.py`` (method
``_compute_texture_pages``) as:

.. code-block:: python

   numtex = pow((10000 / x_res_a_terra), 2) / (tex_size * tex_size * ratio)
   numtex_x_area = (numtex * area_model) / 100
   tex_num = max(1, round(numtex_x_area, 0))

Where the code variables map to the published notation as:

- ``x_res_a_terra`` → :math:`r_{\text{target}}` (default 1.26)
- ``tex_size`` → :math:`s_{\text{tex}}` (default 4096)
- ``ratio`` → :math:`r_{\text{uv}}` (default 0.6)
- ``area_model`` → :math:`A_{\text{tile}}`, from ``chunk.model.area()``

The constant ``10000`` is :math:`L_{\text{ref}}` in mm.

Why these defaults
==================

- **1.26 mm²/texel** (target density): empirically determined through
  iterative testing on Head Mounted Displays and desktop screens with domain
  experts. At this density (~0.67–0.87 texels per mm² of real surface) fine
  details — mortar texture, surface weathering, painted decoration — stay
  clearly visible during close-range immersive inspection while keeping
  rendering performance acceptable. Across the Amba Aradam digital replica the
  achieved density stayed within **1.15–1.32 mm²/texel** (mean ~1.25).
- **4096 px** (:math:`s_{\text{tex}}`): chosen for broad platform
  compatibility — deployable on web browsers, mobile devices and entry-level
  HMDs without exceeding memory limits. :math:`8192^2` is feasible on high-end
  hardware.
- **0.6** (:math:`r_{\text{uv}}`): the median UV-space efficiency observed
  across the dataset; automatic UV parameterization in Metashape leaves ~40 %
  of the atlas unused (island spacing, seam allowances, packing). Adjust it if
  a different unwrapping strategy is used.

.. seealso::

   - Tool reference: :doc:`/reference/tools/metashape-tool`
   - How-to (workflow context): :doc:`/how-to/digital-replica/phase-3-texturing`
   - Rationale: :doc:`digital-replica-rationale`
   - Publication: `Demetrescu et al. 2026 <https://doi.org/10.3390/rs18020203>`__
     — Equation (1) and Supplementary Code S1
