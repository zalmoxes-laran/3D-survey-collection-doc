.. _lod-generator:

.. _LODgenerator:

LOD generator
=============

.. _LODgeneratorFIG:

.. figure:: /img/LODgenerator.jpg
   :width: 400
   :align: center

   LOD generator panel


This panel (:numref:`Fig. %s <LODgeneratorFIG>`) consents to generate Levels of Details (LODs) of a selected mesh.
This type of tool helps manage large and detailed datasets, such as a mesh obtained through photogrammetry, or mesh from laser scanner.

To use this tool the user needs to first indicate the *LOD0* object, that is the mesh with the highest level of detail within the *.blend* file.
To do this, first select the object and, then press the *LOD 0 (set as)* button to designate it as the *LOD 0* object.

Before generating LODs some steps need to be follow:

- set the number of LODs by entering the correct value under the *LOD 0 (set as)* button;
- select the *Pad* option to activate the *Paddin ratio* for LOD creation;
- set the *Decimation ratio*;
- set the *Resolution* of the baked texture;
- indicate the path of the folder where LOD(s) will be saved.

.. admonition:: Remember

 Before closing the path window, it is recommended to uncheck the *relative path* option in the export window settings.
 Alternatively, within the export panel of 3DSC, it is possible to directly paste the entire path into the empty field and then confirm by pressing the *Enter* button.



After all these options have been set, pressing the *generate* button will create LODs in the desired folder.

If necessary, *LOD generator* tool permits to create a group of LODs, by clicking on the *LOD clusters* button, and remove it, by pressing the *X* button.

The *FBX* button allows to export LODs’ cluster in FBX format in the folder previously indicated.
