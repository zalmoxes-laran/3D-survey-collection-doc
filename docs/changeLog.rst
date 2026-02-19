Change Log
==========

.. _NewFeatures:

New Features:
-------------

- Circumcenter Tool: A new tool that allows you to extract circumferences from three designated points on a mesh. This is particularly useful for reconstructing circular and curved elements such as columns and apses from fragmentary data.

- Quick Utils – Flip X and Y Command: Added a function that enables you to invert the X and Y coordinates of selected elements. This is crucial when importing data from total stations where the X and Y axes are swapped. This adjustment is available in Quick Utils, through the dedicated Invert x and y panel.


Improvements:
-------------

- Cesium VTK Tiles Workflow: Added a full Cesium export pipeline with VTK dependency checks/install actions, native quadtree/octree split backend (3D Tiles 1.1), multi-mesh batch export, parent tileset stitching, auto/custom TEMP workspace, and live progress/statistics reporting in the panel.
- Quick Utils UI Refactor: Advanced utility tools (Rotation Constrained, Circle from 3 Points, Alignment Orientation, Texture Smart Mapping) are now root-level panels in the 3DSC sidebar, while Quick Utils keeps miscellaneous commands in a dedicated panel.
- Segmentation Workflow Update: Cutter grids are centralized in the ``_cutter`` root collection, Multi-cutter now supports selected-cutter subsets with automatic fallback to all available cutters, and docs/help links now include dedicated segmentation anchors.
- Color Correction Hardening: node lookup is now robust against renamed nodes (graph/type-based), fixing the ``'bool' object has no attribute 'name'`` crash. The apply flow now keeps an original-texture backup while promoting baked ``cc_image`` output.
- Model Inspector Hardening: geometry/texture/mean-res statistics now handle missing materials/textures safely by default, with optional Strict mode, optional auto-prompt export after MeanRes, and a dedicated Export Stats button.

- Direct Mesh Import in LOD Manager: The LOD Manager now supports direct mesh imports, instead of importing objects. This allows local objects to be attributed with specific values, such as chronology, using the Extended Matrix Tool. This enhancement also enables objects with linked levels of detail (LOD) to be repositioned to preferred coordinates, rather than being fixed at 0,0,0.


Reactivated and Enhanced Features:
----------------------------------

- Color Correction Node Reactivation: The Color Correction node has been reactivated. This tool is particularly effective on models created using photogrammetry. It is recommended to apply color correction before creating levels of detail (LOD) or, alternatively, to recalculate the LOD after applying color correction.

- Shifting System Improvements: The Shifting function now allows external loading and saving of Shift.txt files. Additionally, it can synchronize with the Blender GIS add-on, ensuring better alignment and geographic positioning of your 3D data.
