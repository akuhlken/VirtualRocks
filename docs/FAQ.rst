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

----

What types of images can I use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Our app works for images of type **jpg, png, and tiff**.
For Colmap, it is recomended that images include GPS information in their metadata.

----

No Attribute error in pymeshlab?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Try running ``pip install pymeshlab -U`` to update the package. If this fails, go to the `pymeshlab <https://pymeshlab.readthedocs.io/en/latest/>`_
documentation and find and replace the updated method or variable names. :ref:`Pymeshlab frequently changes their documentation <meshlab>`.

You can also try creating a python script to run ``pymeshlab.replace_pymeshlab_filter_names('/path/to/my/script.py')``.

----

FileNotFoundError when starting the app?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This is because Python could not be found at the location specified by the **PYTHONPATH** constant in :ref:`main.py <main>` 
and :ref:`ReconManager.py <ReconManager>`. The app expects Python to be located in `AppData\\Local\\Programs\\Python\\Python311`. 
There are two solutions to this:

* Uninstall Python and then re-run the binary installer **(recomended)**.
* Run ``where python`` in combination with ``python --version`` and then modify the **PYTHONPATH** constant in :ref:`main.py <main>` and :ref:`ReconManager.py <ReconManager>` to the location returned by the ``where python`` command.


.. note::
    If the ``where`` command cannot find Python or ``--version`` does not return `3.11.5`, you may need to install it. If you already have Python 3.11.5 installed, 
    add it to the system PATH. Both the install and system PATH management will be done automatically by running the **VirtualRocks** binary installer.

