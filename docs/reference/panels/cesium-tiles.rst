.. _cesium-tiles:

.. _CesiumTiles:

Cesium Tiles
============

The *Cesium Tiles* panel exports selected mesh data to Cesium 3D Tiles with two backends:

- *Native Split* (recommended): performs quadtree/octree splitting directly in Blender and writes 3D Tiles 1.1 hierarchy.
- *VTK Writer*: uses ``vtkCesium3DTilesWriter`` when available in the Blender Python environment.

**Dependency and environment checks**

The panel includes a *VTK Dependency Check* section that verifies:

- VTK installation and supported version range;
- availability of Cesium writer symbols;
- optional ``proj.db`` support for EPSG CRS transforms.

If dependencies are missing, install buttons are exposed directly in the panel (same approach used by other dependency-aware tools in 3DSC).

**Source modes**

- *Export active mesh*: exports from current Blender mesh object(s).
- *Use existing OBJ file*: converts an existing ``.obj`` on disk.

When *Export selected meshes* is enabled, each selected mesh is processed in sequence and exported to its own output subfolder.

**Temporary and output folders**

For intermediate exports, the panel supports two temp modes:

- *Auto (near .blend)*: creates/uses ``3dsc2tileTEMP`` next to the saved Blender file;
- *Custom folder*: user-defined path.

Output is written to the configured *Tiles output folder*. With *Create object subfolder* enabled (recommended), each mesh writes to:

``<output>/<object_name>/``

A dedicated trash button can clear temp/output folder contents without deleting the folders themselves.

**Coordinates and CRS modes**

Three coordinate modes are available:

- *Use SHIFT values*: uses EPSG and XYZ from the SHIFT panel (with optional CRS override);
- *Use local coordinates*: local workflow with geocentric fallback CRS;
- *Use custom coordinates*: user-defined XYZ offset and optional CRS.

If CRS is EPSG-based, PROJ data (``proj.db``) must be available.

**Conversion controls**

Main controls include:

- intermediate format (GLB, glTF + textures, OBJ + MTL);
- tree algorithm (Quadtree/Octree);
- features per tile;
- native min/max tree depth;
- quick presets (*Aggressive hierarchy*, *Balanced*, *Few tiles*).

In some VTK builds, tree-type API is not exposed; in that case Quadtree/Octree UI has no effect for *VTK Writer* backend.

**Advanced hierarchy layout**

With *Native Split* backend, two hierarchy layouts are available:

- *Single JSON*;
- *External sub-tilesets* (nested references).

In external mode, output follows a structure with grouped subtree folders and local tile content (for example ``Data/c00/tileset.json`` plus multiple ``f*.glb`` files in the same subtree folder).

**Tileset Stitcher**

The *Tileset Stitcher* section can build/update a parent tileset JSON in the output root:

- *Auto-update parent tileset after export*;
- manual *Rebuild Parent Tileset* button.

This supports iterative workflows where new mesh tilesets are appended over time and referenced from one parent entry point.

**Live progress and statistics**

During export, the panel displays a lightweight live monitor (without complex progress bar):

- current task and mesh index;
- elapsed time;
- recent operation log;
- last mesh statistics.

Per-mesh summary includes values such as initial faces/vertices, estimated area in m2, detected textures, produced tiles, subtree count, and processing time.

.. admonition:: Remember

   UV atlas is not strictly required to create tilesets. However, valid UVs are required for correct textured rendering in output tiles.
