.. _gpr-representation:

===============================================
Representing geophysical slices in 3DSC
===============================================

3DSC represents a geophysical slice — a ground penetrating radar (GPR)
depth slice, an electrical resistivity (ERT) slice or section, a
magnetic map — as a **textured surface**, not as a point cloud, and not
as a voxel volume. It hangs that surface below a **declared
photogrammetric walking surface**, it reads every format through **one
reading core** shared with EMStudio, and it stops short of saying what
any anomaly *is*. This page explains the four decisions and what
follows from each.

.. contents:: On this page
   :local:
   :depth: 2

What the data actually is
=========================

A GPR processing suite exports a depth slice as a list of amplitudes on
a regular grid. The file extension varies — CSV, GeoTIFF, JPEG — but
the content does not: for each cell of a rectangular grid, one number
saying how strongly the radar came back from that depth band.

That matters, because a CSV of coordinates *looks* like a point cloud.
It is not. In the CS07 Tivoli reference dataset each slice is a
complete regular grid of 1492 × 1474 cells at 5 cm — 2 199 208 rows,
exactly the product of the two counts, with no gaps in the indexing.
The Z and depth columns are constant within each file. The only column
carrying information is the amplitude.

About 40 % of those cells carry an **empty** amplitude field. Those are
the cells outside the polygon that was actually surveyed: the footprint
of a real survey is irregular, but it is written out inside a
rectangular bounding grid.

So the file is a raster wearing a table's clothes, and the raster has
holes in it.

The other surveys 3DSC was measured against say the same thing in other
clothes:

- the **UA Ilici** GPR sectors are GeoTIFF rasters, float32, one band,
  0.10 m cells, georeferenced in EPSG:25830, with a nodata value for the
  cells outside the survey and, in two sectors, a cell at 32767 where
  the instrument saturated. They carry no depth: ``mean_v2`` and
  ``sqmean_v2`` are products (mean amplitude, mean of the squares), not
  depth bands;
- the **Alcudia** stack of the same site is 601 screenshots of the GPR
  program, one every 5 mm down to 3 m. A screenshot is a picture of a
  plot, but its plot box sits on the same pixels in all 601, and the
  metres of its axes are printed on it: one frame declared for the
  stack turns every capture into a placed slice;
- the **Basilica Iulia** ERT is a set of headerless ASCII matrices: six
  horizontal slices named by their depth band in centimetres
  (``100-150cm.ASC``) and six vertical sections (``VERT1`` … ``VERT6``),
  each with a grid of its own. The values are **integers 0–255: the
  indices of the colour bar** of the report's figures, not ohm-metres.
  The files say neither their size nor their position; the report does
  (92 × 50 m for the slices, 50 or 92 m by 8 or 9 m for the sections).

What 3DSC does with the last case is the rule for all of them: the
values stay as they are, and what the files do not say is **declared**
— the extent, each section's size, the frame of a capture, and a
*value scale* (1–255 standing for 0–3500 Ω·m, read off the colour bar,
low confidence). A declared scale is written as a declaration in the
manifest and in every stamp, never as a measure.

Why a textured surface
======================

Three representations were available.

A **point cloud** — one vertex per cell — costs 2.2 million vertices
per slice, 88 million for a forty-slice stack. Blender exhausts memory
long before that finishes allocating.

A **voxel volume** is the intuitive answer for stacked depth data, and
it is the wrong one here. Blender has no Python interface for authoring
OpenVDB grids, so it would mean an external dependency; 88 million
voxels are expensive to ray-march; and, more to the point, it does not
give the archaeologist what they actually work with, which is a plan
view they can trace on.

A **textured surface** costs four vertices and one 2D image. The
irregular survey footprint comes for free: cells with no amplitude
become transparent in the texture, so the outline of the survey is a
property of the image rather than something that has to be culled from
geometry.

The intermediate form is a PNG stack plus a JSON manifest. This is
deliberate on two counts. The conversion happens once — re-importing
reads the manifest — and the cache is two orders of magnitude smaller
than the source, which makes it the practical form to archive and pass
around. It is also the shape in which rasterised stacks already arrive
from other projects, so the CSV reader and the image reader converge on
a single representation and the scene-building code has one path.

.. admonition:: Remember

   The reasoning above holds for **processed depth slices**. Raw
   radargrams really are sparse data along profiles, and would need a
   different representation. 3DSC does not attempt them.

A vertical section is the same surface standing up: an upright plane,
its length along the line, its depth downwards. The files of a section
do not say where its line runs on the ground — the Basilica's report
draws the lines on a sketched plan — so 3DSC stands it along X from the
stack's origin, says so, and leaves the placing to you.

Depth is measured from the ground, not from zero
================================================

A slice is a reading taken below the surface the instrument walked on.
Where that surface is not level — which is to say, nearly always — a
horizontal plane at −1 m is one metre below the ground at no point in
particular.

The method 3DSC implements comes from the Tres Tabernae case study
[Ronchi2023]_: fit a surface to the digital elevation model along the Z
axis only, and offset it downwards by the depth of the slice, so that a
reading one metre down sits one metre below *that* point of the
photogrammetric record.

3DSC bakes that construction once instead of leaving it as live
modifiers on every slice, for two reasons.

The first is cost made visible. Following terrain with a subdivided
plane needs enough vertices to do it: the published workflow used ten
subdivision levels, which is on the order of a million faces **per
slice**. Baking turns that into an explicit number — a grid resolution
the user chooses and can see the consequences of.

The second is the one that decides the architecture. **The offset
between one slice and the next is a pure vertical translation.** Two
slices draped on the same terrain differ only by where they sit on the
Z axis. So the baked surface can be shared: every slice object points
at the same mesh and carries its own depth as an object transform.
Forty slices cost one surface. This is what makes it safe to hang a
deep stack below a twenty-million-polygon photogrammetric model, which
is otherwise the obvious way to bring Blender down.

Two modes are offered. A **regular grid** over the slice extent,
dropped onto the ground by ray casting, decouples the drape resolution
from the density of the terrain model and gives exact texture
coordinates. Duplicating the **terrain geometry** itself, decimated to
a triangle budget, is there for when the terrain's own topology carries
something a regular grid would cut across. In both cases the work is
done on a copy: the declared ground object is never touched.

Declaring the ground is part of the method, not a convenience. A drape
is an assertion that these depths are measured from *that* recorded
surface, and the assertion should be attributable to the
photogrammetric document it rests on. 3DSC therefore records which
object was used and whether it was explicitly declared.

.. _gpr-core-source:

One reading core, two programs
==============================

The code that reads the slices — the CSV, GeoTIFF, ASCII, point and
screenshot readers, the depth parsing, the colour ramps, the cache and
its manifest, the identities and the stamps — is not 3DSC's own. It is
``geofisica_core``, the core of the **geophysics package** of the
Extended Matrix (``profiles/geofisica/code/geofisica_core`` in the
``em-profiles`` repository), the same code EMStudio runs when it brings
a stack in. Until 1.7.0-dev.66 3DSC had its own ``gpr_core.py``; it is
gone.

3DSC does not install the package or depend on EM Tools to get it.
The core is **embedded** in the add-on, in ``importer/_vendor/geofisica_core``,
as a copy of one commit of ``em-profiles``:

- ``scripts/geofisica_core.lock.json`` names the commit and the digest
  of the copy (a sha256 over the paths and digests of its ``.py``
  files);
- ``SOURCE.json`` beside the copy says the same, so the core knows it is
  a copy and of which commit;
- the copy is made only by ``scripts/vendor_geofisica_core.py``, from
  the committed tree of that commit, never from working files; the
  tests, the build and the release workflow refuse a copy whose digest
  is not the lock's.

Nothing of the reading is written twice. A correction is made once, in
the package, and reaches 3DSC when the lock is moved to the new commit.
The core needs neither Blender nor s3dgraphy: 3DSC adds only the
Blender side — the panel, the planes, the drape, the shift.

What the core writes it **stamps**: every PNG of a cache and its
manifest leave with ``<file>.stamp.json`` beside them, in the
``dtcstamp`` format — the source files they were made from by digest,
the parameters (ramp, percentiles, declared scale), and the software:
3DSC first, with its version and commit, then the core, with the
``em-profiles`` commit it was copied from. The same stack read by
EMStudio and by Blender is the same cache, named by the digest of its
sources and parameters, with the same stamps. The drape is not
stamped: it is a mesh inside the ``.blend``, not a file, and its
parameters are recorded on the stack's empty.

Where the importer stops
========================

A GPR amplitude map is evidence. A wall is an interpretation. The
distance between the two is an archaeological act, and no importer is
entitled to perform it.

The Extended Matrix has a category for exactly this situation. In the
EMW-geo workflow [Ronchi2023]_, GPR anomalies are formalised as **USD**
— *documentary stratigraphic units*, the category for deferred
observation, the same status as a photograph of a wall that no longer
stands. You do not see the structure; you see a map of anomalies from
which a structure can be argued. Interpretive lines and volumes then
become structural virtual units (USV/s), volumes standing for whole
buildings become non-structural ones (USV/n), and excavated masonry
that confirms them is USM.

Mapped onto the s3Dgraphy data model, the chain has four distinct
links, and collapsing them loses information:

**The acquisition** is the event by which the stack entered the study —
a data transfer event in CIDOC CRMdig terms. It describes the life of
the file. *A stack is an acquisition, not something you read.*

**The resource** is the hinge to the file itself, and it is what the
acquisition produced. The same object is legible twice: as bytes on
disk, and as the outcome of an ingestion.

**The document** is a resource elevated to something that can be read —
the wrapper that makes extraction possible. **One slice is one
document.** The grain matters: extraction happens per slice, because
that is what an operator actually looks at.

**The extraction** is the reading. A proxy drawn from a single slice
rests on a single extraction; a proxy whose shape was argued across
several slices rests on several, combined. That is the difference
between an extractor and a combiner in the graph, and it is recorded
rather than guessed at later.

The USD, finally, is the interpreted entity — *a wall running east to
west, attributed to a period*. It says nothing about geophysics, and it
should not: its warrant is the link to the document, and the document
is the geophysical reading.

What 3DSC does, concretely, is give every slice a stable identity as a
document — keyed on its depth band, so it survives a re-export of the
stack and a rename of the ``.blend``. The identity is the core's, the
same EMStudio gives the document of that slice:
``gpr:<stack>#d<top>-<bottom>m`` for a GPR depth band, as it has always
been, ``ert:`` and ``mag:`` for the other methods, ``#s<line>`` for a
vertical section, and ``#<product>`` (``#mean_v2``) when the depth is
not known. When you tag a proxy, 3DSC
records which of those documents were on screen, how many, and the depth
span they cover. It creates no node and no edge. The stratigraphic
unit, its type and its place in the matrix remain yours to declare,
with the Extended Matrix tools.

.. admonition:: Remember

   The feature is designed to make the interpretive step **possible and
   traceable**, not to take it. If a future version ever proposes
   anomalies automatically, that proposal must arrive as something an
   archaeologist accepts or rejects, never as a unit already in the
   graph.

References
==========

.. [Ronchi2023] Ronchi, D., Limongiello, M., Demetrescu, E. & Ferdani,
   D. (2023). *Multispectral UAV Data and GPR Survey for Archeological
   Anomaly Detection Supporting 3D Reconstruction*. Sensors 23(5),
   2769. https://doi.org/10.3390/s23052769
