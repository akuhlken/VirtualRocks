.. _installation:

Installation
-----------------

Binary installer
^^^^^^^^^^^^^^^^

.. note::
    Check out the :ref:`System Requirements <specreqs>` before installing.

To install the **VirtualRocks** desktop app, go to `GitHub releases <https://github.com/kuhlkena/VirtualRocks/releases>`_ 
and download the latest installer. Note that the installer will also install Python 3.11 with its required packages. For the 
best results, **uninstall Python 3.11** if it's already present on your system **before** trying to install. 

----

Downloading from source
^^^^^^^^^^^^^^^^^^^^^^^
Download and extract the source code from the `GitHub <https://github.com/kuhlkena/VirtualRocks>`_.

Install Python 3.11.5 and ensure that it is installed under `AppData\\Local\\Programs\\Python\\Python311` or modify the constant 
**PYTHONPATH** in :ref:`main.py <main>` and :ref:`ReconManager.py <ReconManager>`.

.. warning::
    There's a `known issue <https://github.com/cnr-isti-vclab/PyMeshLab/issues/47>`_ when trying to use pymeshlab on specific versions
    of Python. Pymeshlab will not work with Python downloaded from the Microsoft store or when using Anaconda.

Run pip install for:

* ttkbootstrap
* show_in_file_manager
* matplotlib
* plyfile
* pymeshlab
* open3d

Also requires the installation of `CUDA <https://developer.nvidia.com/cuda-zone>`_, which may or may not already be present.

----

Installing on Linux
^^^^^^^^^^^^^^^^^^^

The source code for the Windows version of Colmap has been enclosed within 
the project under `/scripts`.

To run on Linux, download the Linux version of `Colmap <https://colmap.github.io/>`_. All calls to 
**COLMAP.bat** must be replaced in :ref:`ReconManager.py <ReconManager>` and :ref:`Matcher.py <Matcher>`.

.. note::
    While this should be possible, **VirtualRocks** has not been tested on Linux. This should only be attempted
    by advanced users.