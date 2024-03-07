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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Our app works for images of type jpg, png, and tiff. 


"no attribute" error in pymeshlab?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Try running ``pip install pymeshlab -U`` to update the package. If this fails go to `pymeshlab <https://pymeshlab.readthedocs.io/en/latest/>`_
and attempt to find the updated method or variable names. (pymeshlab frequently changes their documentation)
You can also try creating a python script and run:
``pymeshlab.replace_pymeshlab_filter_names('/path/to/my/script.py')``

using Sphinx for documentation.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Go into the docs directory and type ``make clean html`` to clear the _build directory. After it's done,
run ``make html``. If any errors pop up,,, they shouldn't be there.