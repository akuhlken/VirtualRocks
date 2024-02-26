
VirtualRocks FAQ
-----------------


A list of frequently asked questions (and their answers) regarding the 
**VirtualRocks** application.

Does the app currently work?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

no.


What operating system can I use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**VirtualRocks** only works on Windows due to software dependencies in the 3D mesh generation pipeline. 
If you're a try-hard, then it technically works on Linux too.


"no attribute pure value" error?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Just run "pip install pymeshlab -U".


using Sphinx for documentation.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Go into the docs directory and type "make clean html" to clear the _build directory. After it's done,
run "make html". If any errors pop up,,, they shouldn't be there.