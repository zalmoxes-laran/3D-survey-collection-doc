.. _ColorCorrection:
.. _color-correction:

Color Correction
================


This panel allows the user to apply a material color correction to one or multiple selected objects (:numref:`Fig. %s <ColorCorrectionFIG>`).

.. _ColorCorrectionFIG:

.. figure:: /img/Color_Correction_01.png
   :width: 800
   :align: center

   *Color Correction* panel


To start the procedure, select one or multiple objects and press *create cc setup*.
The setup is non-destructive and uses a shared CC node group across selected materials.
Node discovery is robust: materials are resolved by shader type and graph connections (not by fixed node names).


.. _ColorCorrection02FIG:

.. figure:: /img/Color_Correction_02.png
   :width: 800
   :align: center

   *Color Correction* panel, activation of the three color profile modifiers (*RGB*, *BC*, and *HS*).

When the procedure is activated, the panel changes its layout (:numref:`Fig. %s <ColorCorrection02FIG>`):

- the *remove cc setup* button appears on top of the panel;
- the name of the edited objects (*cc node: test*) is displayed below the *remove cc setup* button itself;
- a new set of buttons complete the rest of the panel.

Three buttons (*RGB*, *BC*, *HS*) allow to edit the color profile of the texture material.

When *RGB* is pressed the RGB curve appears and it allows to easily change RGB values by moving the line within the graph (:numref:`Fig. %s <ColorCorrection02FIG>`).
The interaction with the curve is similar to that of a standard image editor.

.. _ColorCorrection03FIG:

.. figure:: /img/Color_Correction_03.png
   :width: 800
   :align: center

   *Brightness* and *Constrast* modifiers


When *BC* is pressed, the *Brightness* and *Constrast* sliders appear (:numref:`Fig. %s <ColorCorrection03FIG>`).


.. _ColorCorrection04FIG:

.. figure:: /img/Color_Correction_04.png
   :width: 800
   :align: center

   *Hue* and *Saturation* modifiers


Similarly, when *HS* is pressed, the *Hue*, *Saturation*, and *Value* sliders are displayed at the center of the panel.

Below the *RGB*, *BC*, and *HS* buttons, three additional buttons allow to change the visualization of the material applied to the geometry: *original* displays the original material of the selected object(s); *cc_node* shows the material with the temporary color correction applied; and *cc_image* represents the final result, after baking.

To display these three temporary results, select one of the options (*original*, *cc_node*, or *cc_image*) and then press the *Set view mode* button.

.. _color-correction-bake-apply:

The *bake* button allows to bake all the changes made to the original texture, using Blender’s internal bake function.
These changes can be automatically saved by pressing the *save* button.

The *apply cc* button consents to use the new-modified material.
In this case *EM tools* promotes the baked *cc_image* and keeps a backup reference to the original texture for rollback.

By pressing the *remove cc setup* button, located at the top of the *Color Correction* panel, the user can easily restore the original material.

.. _color-correction-troubleshooting:

**Troubleshooting**

- Renamed image/BSDF nodes are supported.
- Materials without a valid Principled/Diffuse color pipeline are skipped and reported.
