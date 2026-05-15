.. _importers:

Importers
=========

.. _ImportersFIG:

.. figure:: /img/Importers.jpg
   :width: 400
   :align: center

   Importers panel

.. admonition:: Remember

   To import georeferenced data in Blender it is important to set the *SHIFT* data, see the :ref:`Shifting` section.



This panel (:numref:`Fig. %s <ImportersFIG>`) allows importing three data categories in Blender: points, objects, and cameras.

In the current UI, the main buttons are displayed in a flat layout:

- *Points as Empty Objects*
- *Multiple objs*
- *Agisoft XML CAMS* (visible only when *Enable Experimental Features* is active)

Each command also includes a *?* button that opens a contextual help popup with an extended description and a link to online documentation.

.. _ImportersFIG_02:

.. figure:: /img/Importers_02.jpg
   :width: 400
   :align: center

   Option of the Importers panel

By clicking the *Points as Empty Objects* button, users can import a 2D/3D point file (*.csv* or *.txt*) as Empty objects in relative or absolute coordinates.
In the import window, users must: first, locate the appropriate file; second, after pressing the *Toggle Region* button (gear icon on the right side), associate the first 4 columns to name/X/Y/Z and define the separator (comma, space, semicolon, :numref:`Fig. %s <ImportersFIG_02>`).

The options *Shift coordinates* and *Has header* allow to: apply SHIFT values to georeferenced data (when SHIFT has been configured in 3DSC/BlenderGIS) and ignore the first line if the source file has a header.

For a full end-to-end walk-through of the point importer (including
the typical total station / GPS mixed-survey workflow and a
step-by-step recipe for **georeferencing local total station points
onto GPS control points**), see the dedicated recipe
:ref:`import-point-data`.


.. _ImportersFIG_03:

.. figure:: /img/Importers_03.jpg
   :width: 400
   :align: center

   Option of the Importers panel related to objects


By clicking on the *Multiple objs* button, 3DSC imports several OBJ objects with a single command.
In the import window, users must:

- locate the appropriate file;
- select the correct options on the right side (default options generally work for standard OBJ files). If files are not *Z Up* and *Y Forward*, choose the correct orientation from the drop-down menus (:numref:`Fig. %s <ImportersFIG_03>`).

For a full end-to-end walk-through of the batch import (including the
``Shift coordinates`` option, georeferenced datasets and common
troubleshooting), see the dedicated recipe :ref:`import-batch-obj`.

The *Agisoft XML CAMS* command is currently experimental and is displayed only when experimental features are enabled.


.. admonition:: Remember

   By default, when objects are imported into Blender using the *Importer* tool of 3DSC, geometries are displayed as *Bounds*.
   To change this display mode, select the *Object* tab, in the Blender's *Properties* panel, then, in the *Viewport Display* panel, select *Display as* -> *Textured* to visualize the objects with their materials.

.. admonition:: Remember

   It is recommended to import objects without textures if they need to be textured later outside Blender.
