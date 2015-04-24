
 
Data Consolidation or Datamerger
================================

After the images are integrated and the measurements are done there remain a few data consolidation tasks.
The ``datamerge`` module provides this functionality. The :ref:`saxsdmerge` commandline tool is one way to use it,
the other is via the ``Leash``. Its main goal is to merge the logfiles with the parameters logged in the 
images and dedector logs.

The result is a table where each images has one row and the collumns are all the available 
parameters fom continuous logs
or logs that log not regularly but only if an image is requested.

This is where future versions may include a compleete HDF export of all relevant data.
