.. _digital-replica-rationale:

==========================================
Why the Digital Replica workflow
==========================================

The **Digital Replica** workflow produces optimised, multi-LOD photogrammetric
models — called *canvas* once decimated — that act as the canonical
*reality-based* layer for stratigraphic annotation, Extended Matrix
integration, and game-engine publication. This page explains the rationale
behind the design choices; for the step-by-step recipes, see the
:doc:`Phase 1 how-to </how-to/digital-replica/phase-1-canvas-creation>`.

.. contents:: On this page
   :local:
   :depth: 2

What is a Digital Replica
=========================

The Digital Replica workflow creates optimized 3D models (called "canvas")
with:

- **Constant mesh density**: 1,000 or 10,000 polygons/m²
- **High-resolution textures**: 1.26 mm²/texel using the
  :doc:`Demetrescu-d'Annibale formula <texture-resolution-formula>`
- **Multiple LODs** (Levels of Detail) for efficient real-time visualization
- **Optimized structure** for stratigraphic annotation projects

The final output is a Reality-Based (RB) file ready for import into
stratigraphic annotation projects using PyArchInit, Extended Matrix, or
other tools.

Why constant polygon density
============================

Photogrammetric meshes coming out of Metashape or RealityCapture have
non-uniform polygon distribution: dense clusters where photos overlapped,
sparse regions where coverage was thin. The Digital Replica workflow
decimates to a **constant 1000 poly/m²** target because this density:

- Provides sufficient detail to recognise most archaeological / architectural
  features at standard viewing distance.
- Stays low enough for efficient editing inside Blender even on modest
  hardware.
- Is **compatible with game engines** (Unreal, Unity, Godot, O3DE) — these
  engines budget vertices per draw call, and a uniform mesh decimates
  predictably for LOD generation.
- **Avoids flipping geometry artifacts** that are common when very dense
  photogrammetric meshes are imported into editing software.

Why segment into tiles
======================

Even at 1000 poly/m² a whole-site mesh is too large to texture in a single
pass. Segmentation into 60–100 m² tiles unlocks:

- **Per-tile texturing**: each tile gets the exact number of texture pages
  computed by the
  :doc:`texture resolution formula <texture-resolution-formula>` — no global
  texel-budget compromise.
- **Parallelism**: tiles texture independently, so the workflow scales to
  large sites and can be resumed if a tile fails.
- **Per-tile LODs**: switching LODs per-tile means high detail near the
  camera and low detail in the distance, the same mechanism used by
  open-world game engines.

Why a Reality-Based file
========================

The "RB file" (``[ModelName]_RB.blend``) is the *interface* between
photogrammetry and downstream interpretation. Stratigraphic projects, EM
graphs and dataset publications all **link** the RB file rather than
importing it. This keeps:

- **One source of truth** for the reality-based geometry. Re-textured tiles
  propagate to every annotation project that links the RB file.
- **The interpretation layer (proxy meshes) separate** from the photographic
  reference. Proxies are editable, the RB is read-only by convention.
- **Multiple annotation projects** able to reference the same RB without
  duplicating the (potentially gigabyte-scale) textured geometry.

How it fits into Extended Matrix
================================

The Digital Replica lives inside the **Extended Matrix (EM) folder
structure**:

- Raw photos → ``05_RB/01_RAW/photos/``
- Metashape projects → ``05_RB/02_PROCESSING/metashape/``
- All mesh outputs → ``05_RB/03_Model_Library/[ModelName]/``
- Final RB file → ``05_RB/03_Model_Library/[ModelName]/[ModelName]_RB.blend``
- Stratigraphic annotation project → ``07_SB/[ModelName]_EM.blend`` (links RB)
- EM knowledge graph → ``06_EM/[site].graphml``

For the complete file-by-file location guide, see
:ref:`file_location_appendix`.

The numeric prefixes (``05`` → ``03`` etc.) are intentional: they make
folder paths verbally communicable inside teams ("put it in zero-five,
zero-three"), which matters on phone calls and during site work.

.. seealso::

   - Workflow how-to entry point: :doc:`/how-to/digital-replica/index`
   - Texture math: :doc:`texture-resolution-formula`
   - File locations reference: :ref:`file_location_appendix`
   - Extended Matrix Framework: https://www.extendedmatrix.org
