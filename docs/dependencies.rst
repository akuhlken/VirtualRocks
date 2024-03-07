Dependencies
-------------

**VirtualRocks** has a lot of dependencies (libraries + subprocesses) in order to run properly.

----

.. _colmap:

Colmap
===========

**VirtualRocks** depends on **Colmap**, an open source general-purpose Structure-from-Motion (SfM) and Multi-View Stereo (MVS) pipeline software. 
By running commands in Colmap's `command-line interface <https://colmap.github.io/cli.html>`_ as subprocess, VirtualRocks turns the imported 
images into a point cloud and texture with the touch of a button.

The commands used in :ref:`Matcher.py <matcher>`'s `image2dense` function include:

* `feature_extractor`: extracts different features from the images.
* `exhaustive_matcher`: Perform feature matching after performing feature extraction.
* `mapper`: Sparse 3D reconstruction / mapping of the dataset using SfM after performing feature extraction and matching.
* `image_undistorter`: Undistort images and/or export them for Multi-View Stereo or to external dense reconstruction software, such as CMVS/PMVS.
* `patch_match_stereo`: the longest step, Dense 3D reconstruction / mapping using MVS after running the `image_undistorter` to initialize the workspace.
* `stereo_fusion`: Fusion of patch_match_stereo results into to a colored point cloud.
* `model_converter`: Convert the COLMAP export format into PLY.

`Descriptions for each command taken from Colmap's documentation.`

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

As of initial release, the some of the critical filters in :ref:`Mesher.py <mesher>`'s `dense2mesh` function include...

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
and `matplotlib <https://matplotlib.org/stable/>`_. While less critical to the core functionality of the app, each of these
libraries help to create the app style and allows the app to run smoothly. 


