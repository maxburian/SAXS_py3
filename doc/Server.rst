
The Saxsdog Network
===================

The network may consist of 3 different services. The Saxs Server does the image processing. 
The Saxs Feeder puplishes new file Events and the Saxs Leash controlls an configures the server. 
The server should also be able to be manually started and stoped without the Leash.

.. figure:: Network.*

The Saxsdog Server
------------------
The saxdog server can watch for filesystem events for himself 
or subscribe to a zmq service, The Saxsdog Feeder, that publishes new file names.



The Saxsdog Feeder
------------------

New file events are composed of the following message:

.. code:: json
  
   {
      "command":"New file",
      "argument":"/Path/to/file/"
   }

The Saxsdog Leash
-----------------

The Saxsdog Leash is a user facing controll interface. 
There the user should enter new calibrations and specify the data directoris connected to it. 
During the processing it shows a graph of one of the current images.

It may send the following commands:

Close Queue
~~~~~~~~~~~

Request:

.. code:: json

    {
       "command":"close queue",
       "argument":{"queue id":"id"}
    }

Answer:

.. code:: json

   {
   "result":"queue closed", 
   "data":{
      "queuelength":2349,
      "images processed":2030,
      "queueid":"queue id"
      }
   }

Abort Queue
~~~~~~~~~~~

Request:

.. code:: json

   {"command":"abort queue"}

Answer:

.. code:: json

   {
      "result":"queue stopped emptied and closed",
      "data":{
         "queueid":"id",
         "queuelength":2349,
         "images processed":2030
      }
   }

New Queue
~~~~~~~~~

Request:

.. code:: python

      {
      "command":"new queue",
         "argument":{
            "directory":"directory of data to take into account",
            "calibration":{},
            "maskbin":""
         }
      }
   

Answer:


.. code:: json

   {"result":"new queue", "data":{"queueid":"id"}}
   
   
Send Plot
~~~~~~~~~

Request:

.. code:: json

   {"command":"send plot"}
   
Answer:

.. code:: json

   {
    "result":"plot data",
    "data":{
      "filename":"/name/.tiv" ,
      "header":[" "," "],
      "queuelength":2349,
      "images processed":2030,
      "array":[[0],[0],[0]]
      }
   }

Do All in Directory
~~~~~~~~~~~~~~~~~~~

This puts all existing files in the queue directory into the queue again

Request:

.. code::

   {
      "command":"do all in directory",
      "argument":"directory"
   }
Answer:

.. code::

   {
      "result":"directory refilled queue",
      "data":{
         "queuelength":2349,
         "images processed":2030
         }
   }

   
   
Error
~~~~~

In case of error in the Saxsdog Server it will return an error message:

.. code::

   
   {
   "result":"Error",
   "data":["Error message"]
   }
   
   

.. toctree::
    
   SAXSLeashRequest
   SAXSLeashResult
   
   
   