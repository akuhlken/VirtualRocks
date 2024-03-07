Dependencies
-------------

**VirtualRocks** has a lot of dependencies (libraries + subprocesses) in order to run properly.

----

.. _colmap:

Colmap
===========

**VirtualRocks** depends on **Colmap**, open source software that does things. It's a subprocess.

To learn more about Colmap, check out their documentation: `Colmap Documentation <https://colmap.github.io/>`_


----

.. _meshlab:

Pymeshlab
=========

**VirtualRocks** depends on **pymeshlab**, a Python library that interfaces to MeshLab, to make 3D meshs from point clouds and 
image data.

.. note::
    Pymeshlab often changes filter names when updated. Their current list of filters (including functionality and name) can be 
    found `here <https://pymeshlab.readthedocs.io/en/latest/filter_list.html>`_.

As of 3/7/2024, the some of the critical filters in :ref:`Mesher.py <mesher>`'s `dense2mesh` function include...

* `meshing_decimation_clustering <https://pymeshlab.readthedocs.io/en/latest/filter_list.html#meshing_decimation_clustering>`_ (for point cloud simplification)
* `generate_surface_reconstruction_screened_poisson <https://pymeshlab.readthedocs.io/en/latest/filter_list.html#meshing_decimation_clustering>`_ (poisson mesher)
* `meshing_decimation_quadric_edge_collapse <https://pymeshlab.readthedocs.io/en/latest/filter_list.html#meshing_decimation_quadric_edge_collapse>`_ (mesh simplification)
* `meshing_repair_non_manifold_edges <https://pymeshlab.readthedocs.io/en/latest/filter_list.html#meshing_repair_non_manifold_edges>`_ (removing non-manifold edges)
* `compute_texcoord_parametrization_and_texture_from_registered_rasters <https://pymeshlab.readthedocs.io/en/latest/filter_list.html#compute_texcoord_parametrization_and_texture_from_registered_rasters>`_ (building textures)

To learn more about pymeshlab, check out their documentation: `pymeshlab Documentation <https://pymeshlab.readthedocs.io/en/latest/>`_

To learn more about MeshLab, check out their documentation: `MeshLab Website <https://www.meshlab.net>`_


----

open3d
======

While not critical to the main functionality of the app, the `open3d` library lets users view the point cloud 
before turning it into a 3D mesh.

The controls for the open3d window, taken from the 
`open3d <https://www.open3d.org/docs/latest/tutorial/visualization/visualization.html#Visualization>`_ documentation:
:ref:`open3d controls <open3dcontrols>`

To learn more about open3d, check out their documentation: `open3d Documentation <https://www.open3d.org/docs/latest/index.html>`_


----

Additional libraries
====================

**VirtualRocks** depends on other python libraries, including 
`Ttkbootstrap <https://ttkbootstrap.readthedocs.io/en/latest/>`_,
`plyfile <https://python-plyfile.readthedocs.io/en/latest/>`_,
`show_in_file_manager <https://pypi.org/project/show-in-file-manager/>`_,
and `matplotlib <https://matplotlib.org/stable/>`_. They're used to make the app look good and run smoothly, but are less critical
to functionality.


