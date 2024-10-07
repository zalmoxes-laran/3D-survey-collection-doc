Change Log
==========

.. _NewFeatures:

New Features:
-------------

- Circumcenter Tool: A new tool that allows you to extract circumferences from three designated points on a mesh. This is particularly useful for reconstructing circular and curved elements such as columns and apses from fragmentary data.

- Quick Utils – Flip X and Y Command: Added a function that enables you to invert the X and Y coordinates of selected elements. This is crucial when importing data from total stations where the X and Y axes are swapped. This adjustment can now be made easily within the LOD Manager.


Improvements:
-------------

- Direct Mesh Import in LOD Manager: The LOD Manager now supports direct mesh imports, instead of importing objects. This allows local objects to be attributed with specific values, such as chronology, using the Extended Matrix Tool. This enhancement also enables objects with linked levels of detail (LOD) to be repositioned to preferred coordinates, rather than being fixed at 0,0,0.


Reactivated and Enhanced Features:
----------------------------------

- Color Correction Node Reactivation: The Color Correction node has been reactivated. This tool is particularly effective on models created using photogrammetry. It is recommended to apply color correction before creating levels of detail (LOD) or, alternatively, to recalculate the LOD after applying color correction.

- Shifting System Improvements: The Shifting function now allows external loading and saving of Shift.txt files. Additionally, it can synchronize with the Blender GIS add-on, ensuring better alignment and geographic positioning of your 3D data.