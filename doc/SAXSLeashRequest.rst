.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

.. _required:

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
-------------------------

:Type:
  string
:values:
  [close, abort, new, get, plot, plotdata, readdir, stat, listdir, putplotdata, fileslist, mergedata, getmergedata]

:Required:
  True
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`command <command>`']

Example JSON: 

.. code:: json

    {"command": "close"}

.. _argument:

argument
-------------------------

:Type:
  object
:Contains:
  :ref:`calibration <calibration>`, :ref:`mergeconf <mergeconf>`, :ref:`data <data>`, :ref:`directory <directory>`
:Required:
  False
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`argument <argument>`']

Example JSON: 

.. code:: json

    {"argument": {}}

.. _calibration:

calibration
-------------------------

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

.. _mergeconf:

mergeconf
-------------------------

Datamerger Configuratioin


:Type:
  object
:Contains:
  :ref:`/<DataConsolidationConf.json#>`
:Required:
  False
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`argument <argument>`'][':ref:`mergeconf <mergeconf>`']

Example JSON: 

.. code:: json

    {"mergeconf": {}}

.. _data:

data
-------------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`argument <argument>`'][':ref:`data <data>`']

Example JSON: 

.. code:: json

    {"data": {}}

.. _directory:

directory
-------------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <reqroot>` [':ref:`argument <argument>`'][':ref:`directory <directory>`']

Example JSON: 

.. code:: json

    {"directory": {}}

.. _sign:

sign
-------------------------

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
-------------------------

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

