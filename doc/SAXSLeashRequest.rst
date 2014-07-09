.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

.. _root:.. _required:

 The ':red:`*`' signifies a required Field.

Schema for requests from Saxs Leash to Saxs Server


:Type:
  object
:Contains:
  :ref:`command <command>`:red:`*`, :ref:`argument <argument>`
:Required:
  True
:JSON Path:
  :ref:`# <root>` 

Example JSON: 

.. code:: json

    {"command": "close"}

.. _command:

command
--------------------

:Type:
  string
:values:
  ``[u'close', u'abort', u'new', u'plot', u'readdir', u'stat']``

:Required:
  True
:JSON Path:
  :ref:`# <root>` [':ref:`command <command>`']

Example JSON: 

.. code:: json

    {"command": "close"}

.. _argument:

argument
--------------------

:Type:
  object
:Contains:
  :ref:`directory <directory>`, :ref:`calibration <calibration>`
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`argument <argument>`']

Example JSON: 

.. code:: json

    {"argument": {}}

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

