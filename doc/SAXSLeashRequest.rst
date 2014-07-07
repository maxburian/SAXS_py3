.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

.. _root:


JSON Configuration File
=======================

.. _required:

 The ':red:`*`' signifies a required Field.

Schema for requests from Saxs Leash to Saxs Server


:Type:
  object
:Contains:
  :ref:`command <command>`, :ref:`argument <argument>`
:Required:
  True
:JSON Path:
  :ref:`# <root>` 

Example JSON: 

.. code:: json

    {}

.. _command:

command
--------------------

:Type:
  string
:values:
  [u'close queue', u'stop queue', u'new queue', u'send plot', u'do all in directory']

:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`command <command>`']

Example JSON: 

.. code:: json

    {"command": "close queue"}

.. _argument:

argument
--------------------

:Type:
  object
:Contains:
  :ref:`queue id <queue id>`, :ref:`directory <directory>`, :ref:`calibration <calibration>`, :ref:`maskbin <maskbin>`
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`argument <argument>`']

Example JSON: 

.. code:: json

    {"argument": {}}

.. _queue id:

queue id
--------------------

String that uniquely indentifies a queue


:Type:
  string
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`argument <argument>`'][':ref:`queue id <queue id>`']

Example JSON: 

.. code:: json

    {"queue id": ""}

.. _directory:

directory
--------------------

Directory this queue is going to use. New files in other directories are going to be ignored.


:Type:
  string
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`argument <argument>`'][':ref:`directory <directory>`']

Example JSON: 

.. code:: json

    {"directory": ""}

.. _calibration:

calibration
--------------------

Calibrarion data according to :ref:`calib`


:Type:
  object
:Contains:
  :ref:`/<schema.json#>`
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`argument <argument>`'][':ref:`calibration <calibration>`']

Example JSON: 

.. code:: json

    {"calibration": {}}

.. _maskbin:

maskbin
--------------------

the mask file binary encoded as base64


:Type:
  string
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`argument <argument>`'][':ref:`maskbin <maskbin>`']

Example JSON: 

.. code:: json

    {"maskbin": ""}

