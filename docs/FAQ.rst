FAQ
----


A list of frequently asked questions (and answers) regarding the 
**VirtualRocks** application.


What operating system can I use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**VirtualRocks** only works on Windows due to software dependencies in the 3D mesh generation pipeline. 
It may also work on Linux, but it hasn't been tested and installing dependencies is more difficult.

.. warning::
    This app requires an NVIDA graphics card with `CUDA <https://developer.nvidia.com/cuda-zone>`_ installed.


What types of images can I use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Our app works for images of type jpg, png, and tiff.
For colmap it is recomended that images include GPS information in their metadata.


"no attribute" error in pymeshlab?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Try running ``pip install pymeshlab -U`` to update the package. If this fails go to the `pymeshlab <https://pymeshlab.readthedocs.io/en/latest/>`_
doc and attempt to find the updated method or variable names. (pymeshlab frequently changes their documentation)
You can also try creating a python script which runs: ``pymeshlab.replace_pymeshlab_filter_names('/path/to/my/script.py')``

FileNotFoundError when starting the app?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This is most likely caused when starting the app if python could not be found at the location 
specified by the **PYTHONPATH** constant in main.py and in ReconManager.py. The app expects python to be located in:
AppData\\Local\\Programs\\Python\\Python311. There are two solutions to this:
* Uninstall python and then re-run the binary installer (recomended)
* Run ``where python`` in combination with ``python --version`` and then modify the **PYTHONPATH** constant in main.py and ReconManager.py to the location 
returned by the where command.

.. note::
    If the ``where`` command cannot find python or ``--version`` does not return 3.11.5, you either need to install it or if you already have it installed, 
    add it to the system PATH. Both of which will be done automatically by running the VirtualRocks binary installer

Using Sphinx for documentation.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Go into the docs directory and type ``make clean html`` to clear the _build directory. After it's done,
run ``make html``. If any errors pop up,,, they shouldn't be there.