.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

:.. _required:

 The ':red:`*`' signifies a required Field.

Schema for requests from Saxs Leash to Saxs Server


:Type:
  object
:Contains:
  :ref:`command <command>`:red:`*`, :ref:`argument <argument>`, :ref:`sign <sign>`, :ref:`time <time>`
:Required:
  True
:JSON Path:
  * :ref:`# <reqroot>` 

Example JSON: 

.. code:: json

    {"command": "close"}

.. _command:

command
--------------------

:Type:
  string
:values:
  ``[u'close', u'abort', u'new', u'get', u'plot', u'plotdata', u'readdir', u'stat', u'listdir', u'putplotdata']``

:Required:
  True
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`command <command>`']

Example JSON: 

.. code:: json

    {"command": "close"}

.. _argument:

argument
--------------------

:Type:
  object
:Contains:
  :ref:`directory <directory>`, :ref:`threads <threads>`, :ref:`calibration <calibration>`, :ref:`data <data>`
:Required:
  False
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`argument <argument>`']

Example JSON: 

.. code:: json

    {"argument": {}}

.. _directory:

directory
--------------------

Directory this queue is going to use. New files in other directories are going to be ignored.


:Type:
  array() items: 
:Required:
  False
:Default:
  [u'.', u'', u'']
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`argument <argument>`'][':ref:`directory <directory>`']

Example JSON: 

.. code:: json

    {"directory": [".","",""]}

.. _threads:

threads
--------------------

:Type:
  integer
:Required:
  False
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`argument <argument>`'][':ref:`threads <threads>`']

Example JSON: 

.. code:: json

    {"threads": 0}

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
  * :ref:`# <reqroot>` [':ref:`argument <argument>`'][':ref:`calibration <calibration>`']

Example JSON: 

.. code:: json

    {"calibration": {}}

.. _data:

data
--------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`argument <argument>`'][':ref:`data <data>`']

Example JSON: 

.. code:: json

    {"data": {}}

.. _sign:

sign
--------------------

Signature of request


:Type:
  string
:Required:
  False
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`sign <sign>`']

Example JSON: 

.. code:: json

    {"sign": ""}

.. _time:

time
--------------------

time in seconds (pythons time.time())


:Type:
  number
:Required:
  False
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`time <time>`']

Example JSON: 

.. code:: json

    {"time": 0}

