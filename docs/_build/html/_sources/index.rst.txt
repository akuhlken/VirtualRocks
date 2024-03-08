.. VirtualRocks documentation master file, created by
   sphinx-quickstart on Wed Jan 31 14:18:26 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

VirtualRocks
========================================

.. figure:: media/header.png
   :alt: mojave model
   :height: 150 px
   :width: 1000 px
   :scale: 100 %
   :align: left


**VirtualRocks** is a CS senior capstone project made over the course of the 2023/24
school year. It serves as a pipeline to turn a set of user-uploaded images into a set of tiled 3D meshes with 
high quality textures, optimized for viewing on VR headsets.

**VirtualRocks Unity** is a partner `virtual reality application <https://github.com/kuhlkena/VirtualRocksUnity>`_
created in Unity designed to view and navigate the large models created by the `VirtualRocks` app using distance 
culling and shaders.

----

Getting Started
---------------
* Install the VirtualRocks application :ref:`here <installation>`.
* Create a new project inside a directory that will be used as the project workspace.
* Add your images. Images should have a high degree of overlap with minimal background (Ideally between 100-500 images).
* Run the :ref:`matcher <colmap>` and :ref:`mesher <meshlab>`.
* To view your models in VR, follow the instructions in :ref:`Unity installation <unity>`.

.. figure:: media/start.png
   :alt: mojave model
   :height: 350 px
   :width: 500 px
   :scale: 100 %
   :align: left

.. figure:: media/main.png
   :alt: mojave model
   :height: 350 px
   :width: 500 px
   :scale: 100 %
   :align: left


Acknowledgments
---------------
The default models in **VirtualRocks Unity** are sourced from different projects and research conducted by
the `Geology Department <https://www.whitman.edu/academics/majors-and-minors/geology>`_ at Whitman College.

The Twin Sisters and Mojave models were created by Lyman Persico, Weston Elgin Hw model by Coden Stark, and
Mt Carmel Junction model by Morgan Sharp.


.. toctree::
   :hidden:
   :caption: Contents:
   :maxdepth: 2

   FAQ
   Installation
   Samples
   unity
   dependencies
   reference/references
   license
   
----

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
