
The Saxsdog Network
===================

The network may consist of 3 different services. The "Saxsdog Server" does the image processing. 
The "Saxs Feeder" puplishes new file Events and the "Saxs Leash" controlls an configures the server. 
The server should also be able to be manually started and stoped without the Leash.

.. figure:: Network.*

The Saxsdog Server
------------------

The Saxdog Server is the program that is started on the processing computer (node). 
It may subscribe to a "new file" event service. 

.. command-output::  saxsdogserver --help

The Saxs Leash
--------------

The "Saxs Leash" client can issue the commands for the Saxsdog Server. It has a commandline interface only, for now.

.. command-output::  saxsleash --help

Most of the commandline options are apout the ``plot`` command, but in order to visualize 
the processed data, one has to send the commands to setup a calibration.

New
~~~

.. code::
   
   # saxsleash new cal.json data/AAA_integ.msk data/

The ``new`` command loads a calibration and starts the queue to receive new files. It requires 3 arguments:

1. Calibration file. as in :ref:`calib`,
2. mask file,
3. directory where the image files are or are going to be.

If there is a queue running, this command will abort the other one and replace it.
 One server can have only one queue at a time.

Plot
~~~~

.. code::
   
   # saxsleash plot

The plot command will grab the next image and show a plot of the result in a window. 
This command will be repeated until the user interrupts it with ``Ctrl-C``.

Close
~~~~~

.. code::
   
   # saxsleash close

Closes the queue. Which means, the server will process what is left in the queue but ignore all new files.

Abort
~~~~~
.. code::
   
   # saxsleash abort

The abort command will close the queue  and stop all data processing processes.
It will only wait for each process to finish the picture they started before. 
The remaining pictures in the queue are ignored.
 
Stat
~~~~
.. code ::

   # saxsleash stat

Return basic statistics data about the processes.

Read Dir
~~~~~~~~

.. code::

   # saxsleash readdir

This command will put all the images in the configured directory into the queue.
This is usefull to reprocess pictures.

The Saxsdog Network Protocol
----------------------------

.. toctree::
   SAXSProtocol
   
   
   