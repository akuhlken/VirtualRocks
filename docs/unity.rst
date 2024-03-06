
Unity Help
-----------------

**VirtualRocks** makes tiled meshes that, when imported and compiled in **Unity**, can be viewed on a VR headset.

1: Getting the Unity project
***********************************

* VirtualRocks Unity: `<https://github.com/kuhlkena/VirtualRocksUnity>`_ 
* Unity Hub: `<https://unity.com/download>`_

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/9LbwMpaqgBI?si=YWzTz5JiuyzsvKT-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

----

2: Add new scene
***********************

* Create a copy of sample scene folder.
* Rename new folder, the unity scene, and the sampleMat to something unique.
* Switch the the newly created scene by double clicking.
* Drag the models and textures from your out folder to the meshes folder for your scene, wait for them to import.
* Drag and drop the tile prefab files into the map folder in the scene previewer.
* With prefabs selected right click and under "prefab" select "unpack completely".
* Right click and select children, then drag into the map folder again.
* Now use the searchbar in the scene previewer to find and delete all the now empty tile opjects.
* Select all the "default" objects and add a sphere collider.
* Then mark as static and turn off cast and recieve shadows.
* Finally dissable the mesh renderer for all "default" objects
* Move loy_poly prefab into scene, unpack, and mark as static.
* Disable cast and recieve shadows for low_poly.
* Set the texture for the special meterial in the scene folder to be the low_poly.jpg
* Set the material for the low_poly mesh in the scene to be the special material.
* Scale and rotate all meshes to be roughly the size of the white plane, then remove the plane for the scene.
* Save and add the new scene to the build.
* Navigate to the menu scene and add a new option to the dropdown with your scene name.
* Finally edit the LoadScene script and add a conditional for the index of your scene in the dropdown.
* Save the menu scene.

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/MIyeqbPsDwk?si=WDd7hu4G6ALRu7F_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

----

3: Build to headset
*************************

* Oculus desktop app: `<https://www.meta.com/quest/setup/>`_ 
* Note: you may need to enable developer mode on your quest headset `<https://youtu.be/0sOqjnjkn-g?si=ehpftVt5r_5uk_OD>`_ 

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/yHr-8eaQD2o?si=u7X5OwBDjSiwU3QJ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

----