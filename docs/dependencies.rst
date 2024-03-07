Dependencies
-------------

**VirtualRocks** has a lot of dependencies (libraries + subprocesses) in order to run properly.

.. _colmap:

Colmap
===========

**VirtualRocks** depends on **Colmap**, open source software that does things. It's a subprocess.

To learn more about Colmap, check out their documentation: `Colmap Documentation <https://colmap.github.io/>`_


.. _meshlab:

Pymeshlab
=========

**VirtualRocks** depends on **pymeshlab**, a Python library that interfaces to MeshLab, to make 3D meshs from point clouds and 
image data. Different filters/functions from `pymeshlab` are used in :ref:`Mesher.py <mesher>` (in the `dense2mesh` function).

.. note::
    Pymeshlab often changes filter names when updated. Their current list of filters (including functionality and name) can be 
    `here <https://pymeshlab.readthedocs.io/en/latest/filter_list.html>`_.

To learn more about pymeshlab, check out their documentation: `pymeshlab Documentation <https://pymeshlab.readthedocs.io/en/latest/>`_

To learn more about MeshLab, check out their documentation: `MeshLab Website <https://www.meshlab.net>`_


open3d
======

While not critical to the main functionality of the app, the `open3d` library lets users view the point cloud made from their
images using Colmap before turning it into a 3D mesh.

The controls for the open3d window, taken from the 
`open3d <https://www.open3d.org/docs/latest/tutorial/visualization/visualization.html#Visualization>`_ documentation:
:ref:`open3d controls <open3dcontrols>`

To learn more about open3d, check out their documentation: `open3d Documentation <https://www.open3d.org/docs/latest/index.html>`_


Additional libraries
====================

**VirtualRocks** depends on other python libraries, including 
`Ttkbootstrap <https://ttkbootstrap.readthedocs.io/en/latest/>`_,
`plyfile <https://python-plyfile.readthedocs.io/en/latest/>`_,
`show_in_file_manager <https://pypi.org/project/show-in-file-manager/>`_,
and `matplotlib <https://matplotlib.org/stable/>`_. They're used to make the app look good and run smoothly, but are less critical
to functionality.


