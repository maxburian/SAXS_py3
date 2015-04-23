

The Saxsdog Server
~~~~~~~~~~~~~~~~~~
The saxdog server can watch for filesystem events for himself 
or subscribe to a zmq service,
the Saxsdog Feeder, that publishes new file names. The server can process the new images acording to one 
calibration. The server may only have one calibration at a time, it is not designed to be used 
by multiple users at the same time.



The Saxsdog Feeder
~~~~~~~~~~~~~~~~~~

The "Saxsdog Feeder" service offers file events for subscription.
It sould not do anny buffering or preselection, just send a new 
message when any new file was copied and is ready for processing. 
Also when a file is overwritten: Send a message. It should however, 
only send this event, when the file is completly written to the file system.


New file events are composed of the following message:

.. code:: json
  
   {
      "command":"new file",
      "argument":"/Path/to/file/"
   }

The service must be a ZeroMQ ``zmq.PUP`` socket. This code is a simulation of the messages:

.. literalinclude :: ../SAXS/Feeder.py

The Saxsdog Leash
~~~~~~~~~~~~~~~~~

The Saxsdog Leash is a user-facing controll interface. 
There, the user should enter new calibrations and specify the data directories connected to it. 
During the processing, it shows a graph of one of the current images.

It may send the following commands:

Close
-----

Request:

.. code:: json

    {
      "command":"close queue",
      "time":1404979588.715198,
      "sign":"Signature generated for request"
    }

Answer:

.. code:: json

   {
   "result":"queue closed", 
   "data":{  
      "stat": {
         "time interval": 0.8776118755340576, 
         "queue length": 0, 
         "frames per sec": 10.25510279760422, 
          "images processed": 235, "pics": 9
         }
      }
   }

Abort
-----

Request:

.. code:: json

   {  
      "command":"abort queue",
      "time":1404979588.715198,
      "sign":"Signature generated for request"
   }

Answer:

.. code:: json

   {
      "result":"queue stopped emptied and closed",
      "data":{
         "stat": {
            "time interval": 0.8776118755340576, 
            "queue length": 0, 
            "frames per sec": 10.25510279760422, 
            "images processed": 235, 
            "pics": 9
         }
      }
   }

New
---

Request:

.. code:: python

      {
         "command":"new queue",
         "argument":{
            "directory":["path","to","data"],
            "calibration":{},
            "maskbin":""
         },
      "time":1404979588.715198,
      "sign":"Signature generated for request"
      }
   

Answer:


.. code:: json

   { "result":"new queue", 
     "data":{ 
            }
      
   }
   
   
Plot
----

Request:

.. code:: json

   {  "command":"send plot",
      "time":1404979588.715198,
      "sign":"Signature generated for request"
   }
   
Answer:

.. code:: json

   {
    "result":"plot data",
    "data":{
      "filename":"/name/.tiv" ,
      "stat": {
            "time interval": 0.8776118755340576, 
            "queue length": 0, 
            "frames per sec": 10.25510279760422, 
            "images processed": 235, 
            "pics": 9
            },
      "array":[[0],[0],[0]]
      }
   }

Readdir
-------

This puts all existing files in the queue directory into the queue again

Request:

.. code::

   {
      "command":"readdir",
      "time":1404979588.715198,
      "sign":"Signature generated for request"
     
   }
Answer:

.. code::

   {
      "result":"directory refilled queue",
      "data":{
         "stat": {
            "time interval": 0.8776118755340576, 
            "queue length": 0, 
            "frames per sec": 10.25510279760422, 
            "images processed": 235, "pics": 9
         }
      }
   }

Stat
----
Get basic processing statistics.

Request:

.. code::

   {  "command":"stat","argument":{},
      "time":1404979588.715198,
      "sign":"Signature generated for request"}

Answer:

.. code::

   {
   "data": {
      "stat": {
         "time interval": 711.6886098384857, 
         "queue length": 0, 
         "frames per sec": 9.972057866165134, 
         "images processed": 7332, 
         "pics": 7097
         }
       }, 
   "result": "stat"
   }
   
Error
-----

In case of error in the Saxsdog Server it will return an error message:

.. code::

   
   {
   "result":"Error",
   "data":{"Error":"Error message"}
   }
   
   
.. _reqroot:

Request Schema
~~~~~~~~~~~~~~
   
.. include:: SAXSLeashRequest.rst
   
.. _resroot:

Response Schema
~~~~~~~~~~~~~~~
 

.. include:: SAXSLeashResult.rst


.. _consroot:

Datamerge Schema
~~~~~~~~~~~~~~~~


.. include:: DataConsolidationSchema.rst

