
Installation
-----------------

Binary installer
^^^^^^^^^^^^^^^^
To install the VirtualRocks desktop app head to the `GitHub releases <https://github.com/kuhlkena/VirtualRocks/releases>`_ 
and download the latest installer. Note that the installer will also install Python 3.11 with it's required packages and for the 
best results we recomend first uninstalling python 3.11 if it is present on your system. 

.. note::
    Check out the :ref:`System Requirements page <specreqs>` before installing

Downloading from source
^^^^^^^^^^^^^^^^^^^^^^^
Download and extract the source code from the `GitHub <https://github.com/kuhlkena/VirtualRocks>`_
Install Python 3.11.5 and ensure that it is installed under AppData\\Local\\Programs\\Python\\Python311 or modify the constant 
"PYTHONPATH" in main.py and ReconManager.py

.. note::
    Know issue with python downloaded from the Microsoft store and pymeshlab `pymeshlab issue <https://github.com/cnr-isti-vclab/PyMeshLab/issues/47>`_
    as well as issues using anaconda and pymeshlab

Run pip install for 

* ttkbootstrap
* show_in_file_manager
* matplotlib
* plyfile
* pymeshlab
* open3d

Also requires and installation of Cuda wich may or may not already be present.

Installing on Linux
^^^^^^^^^^^^^^^^^^^

The source code for the Windows version of Colmap has been enclosed within 
the project under /scripts, to run on Linux this must be replaced with the 
linux version of `Colmap <https://colmap.github.io/>`_ and all calls to 
"COLMAP.bat" must be repaced in ReconManager.py and Matcher.py

.. note::
    This has not beet tested but should be possible.