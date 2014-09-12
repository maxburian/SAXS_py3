
The Saxsdog Network
===================

The network may consist of 3 different services. The "Saxsdog Server" does the image processing. 
The "Saxs Feeder" publishes new file Events and the "Saxs Leash" controls an configures the server. 
 
.. figure:: Network.*

The SAXSNetwork configuration
-----------------------------
The Saxsdog Server and the Saxsleash have a common configuration file, which tells them how to connect
with each other and which also includes a shared secret for authentication. 
If you want two computers to connect via the Saxsleash you need to have a copy of the file on each of them.

To create such a configuration, use the command:

.. code::
   
   $ saxsnetconf

It will ask for the Feeder 
URL and for the Saxsdog Server URL. Then it will generate a random secret and save the file in
file in ``$Home/.saxdognetwork``.  You will have to copy the file 
to the other computers you need to allow to connect to your network. The secret must be the same on all of them.


.. code ::

   {
      "Server":"tcp://hostname:port",
      "Feeder":"tcp://hostname:port",
      "Secret":"Some large random string."
   }

The authentication is done by hashing the request and the secret including a time stamp. 
The time stamp is checked if it lies within 900 seconds of the servers time.

The Saxsdog Server
------------------

The Saxdog Server is the program that is started on the processing computer (node). 
It may subscribe to a "new file" event service. 

.. command-output::  saxsdogserver --help

The Saxs Leash
--------------

The Leash Program is a GUI to load calibrations into the Saxdog Server and monitor the processing of the data.
It provides a calibration editor, as mask preview and basic data import from :ref:`saxsconverter`. 

The main window has 3 tab cards. The first is for setting up the server, 
the second to review the currently processed data and the third for basic statistics. The command to launch it is.

.. program-screenshot:: Leash  
    :prompt:

Saxs Leash Commandline
----------------------


The "Saxs Leash" client can issue the commands for the Saxsdog Server. 

.. command-output::  saxsleash --help

Most of the command line options are about the ``plot`` command, but in order to visualize 
the processed data, one has to send the commands to setup a calibration.


New
~~~

.. code::
   
   $ saxsleash new cal.json data/AAA_integ.msk data/

The ``new`` command loads a calibration and starts the queue to receive new files. It requires 3 arguments:

1. Calibration file. as in :ref:`calib`,
2. mask file,
3. directory where the image files are or are going to be.

If there is a queue running, this command will abort the other one and replace it.
 One server can have only one queue at a time.

Plot
~~~~

.. code::
   
   $ saxsleash plot

The ``plot`` command will grab the next image and show a plot of the result in a window. 
This command will be repeated until the user interrupts it with ``Ctrl-C``.

Close
~~~~~

.. code::
   
   $ saxsleash close

Closes the queue. Which means, the server will process what is left in the queue but ignore all new files.

Abort
~~~~~
.. code::
   
   $ saxsleash abort

The ``abort`` command will close the queue  and stop all data processing processes.
It will only wait for each process to finish the picture they started before. 
The remaining pictures in the queue are ignored.
 
Stat
~~~~
.. code ::

   $ saxsleash stat

Return basic statistics data about the processes.

Read Dir
~~~~~~~~

.. code::

   $ saxsleash readdir

This command will put all the images in the configured directory into the queue.
This is useful to reprocess pictures.



The Saxsdog Network Protocol
----------------------------

.. toctree::
   SAXSProtocol
   
   
   