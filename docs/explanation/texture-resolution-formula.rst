.. _texture-resolution-formula:

==========================================
Texture resolution formula
==========================================

The **Demetrescu-d'Annibale texture resolution formula** is the algorithm
3DSC uses to compute how many texture pages are needed to texture a
segmented photogrammetric tile at a target ground resolution. It is the
single source of truth for every place in the documentation that quotes the
formula — the Metashape tool reference and the
:doc:`Digital Replica Phase 3 how-to </how-to/digital-replica/phase-3-texturing>`
both link back here.

The formula was published in `Demetrescu et Alii 2026
<https://doi.org/10.3390/rs18020203>`__ and is implemented in the
:doc:`3DSC for Metashape </reference/tools/metashape-tool>` script package.

.. contents:: On this page
   :local:
   :depth: 2

The formula
===========

For a given tile area and target texel size, the number of texture pages
needed to cover the tile is:

.. math::

   N_{\text{tex}} = \frac{(10000 / r_{\text{texel}})^2}{t_{\text{res}}^2 \times ratio}

Where:

- :math:`r_{\text{texel}}` = target resolution in mm/texel
  (typically **1.2 mm** for archaeological VR; default in the script is 1.26 mm)
- :math:`t_{\text{res}}` = texture page resolution in pixels
  (typically **4096**)
- :math:`ratio` = surface coverage efficiency factor (typically **0.6**) —
  accounts for UV-space packing inefficiency

The result :math:`N_{\text{tex}}` is the **number of 4096×4096 texture
pages per 100 m²** of tile surface; scale by tile area to obtain the actual
count.

Worked example
==============

For a **100 m² tile** at **1.2 mm/texel** with **4096 px texture pages** and
**ratio 0.6**:

.. math::

   N_{\text{tex}} = \frac{(10000 / 1.2)^2}{4096^2 \times 0.6} \approx 6

**Result:** 6 textures at 4096×4096 px per 100 m² tile.

Reference table
===============

Indicative texture counts at 1.26 mm/texel, 4096 px pages, ratio 0.6:

.. list-table::
   :widths: 20 20 20 20 20
   :header-rows: 1

   * - Area (m²)
     - Textures (4096px)
     - Total Pixels
     - Est. File Size
     - Resolution
   * - 10
     - 1
     - 16.7 MP
     - 15 MB
     - 1.26 mm/px
   * - 50
     - 3
     - 50.3 MP
     - 45 MB
     - 1.26 mm/px
   * - 100
     - 6
     - 100.6 MP
     - 90 MB
     - 1.26 mm/px
   * - 200
     - 12 (capped)
     - 201.3 MP
     - 180 MB
     - 1.26 mm/px

Reference implementation
========================

The formula is implemented in ``texturize_it.py`` (and in the
``3DSC_MS_GUI.py`` single-file build) as:

.. code-block:: python

   numtex = pow((10000 / x_res_a_terra), 2) / (tex * tex * ratio)
   numtex_x_area = (numtex * area_model) / 100
   tex_num = max(1, round(numtex_x_area, 0))

Where the variables map to the formula as:

- ``x_res_a_terra`` → :math:`r_{\text{texel}}`
- ``tex`` → :math:`t_{\text{res}}`
- ``ratio`` → :math:`ratio`
- ``area_model`` → tile area in m² (computed from the imported mesh)

Why these defaults
==================

The 1.2–1.26 mm/texel target was chosen as the sweet spot for archaeological
and architectural heritage documentation:

- **Sufficient detail** to identify tool marks, inscriptions, and small
  surface features at one-to-one viewing distance.
- **VR-ready** — balances visual quality with the texture-memory budget of
  consumer headsets.
- **Real-time engine compatible** — texture page sizes (4096 px) match the
  upload constraints of Unreal, Unity, Godot and O3DE.
- **Storage-aware** — the table above shows the formula avoids producing
  excessive PNG files even for 200 m² tiles.

The 0.6 ``ratio`` factor empirically accounts for the unavoidable UV-space
waste introduced by atlasing curved or vertical surfaces.

.. seealso::

   - Tool reference: :doc:`/reference/tools/metashape-tool`
   - How-to (workflow context): :doc:`/how-to/digital-replica/phase-3-texturing`
   - Rationale: :doc:`digital-replica-rationale`
   - Publication: `Demetrescu et Alii 2026 <https://doi.org/10.3390/rs18020203>`__
