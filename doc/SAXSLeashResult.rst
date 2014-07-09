.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

.. _root:.. _required:

 The ':red:`*`' signifies a required Field.

Schema for requests from Saxs Leash to Saxs Server


:Type:
  object
:Contains:
  :ref:`result <result>`:red:`*`, :ref:`data <data>`:red:`*`
:Required:
  True
:JSON Path:
  :ref:`# <root>` 

Example JSON: 

.. code:: json

    {"data": {},"result": ""}

.. _result:

result
--------------------

:Type:
  string
:Required:
  True
:JSON Path:
  :ref:`# <root>` [':ref:`result <result>`']

Example JSON: 

.. code:: json

    {"result": ""}

.. _data:

data
--------------------

:Type:
  object
:Contains:
  :ref:`stat <stat>`, :ref:`filename <filename>`, :ref:`array <array>`
:Required:
  True
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`']

Example JSON: 

.. code:: json

    {"data": {}}

.. _stat:

stat
--------------------

:type:
  object


:Contains:
  :ref:`queue length <queue length>`, :ref:`images processed <images processed>`, :ref:`time interval <time interval>`, :ref:`frames per sec <frames per sec>`, :ref:`pics <pics>`
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`stat <stat>`']

Example JSON: 

.. code:: json

    {"stat": {}}

.. _queue length:

queue length
--------------------

:Type:
  integer
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`queue length <queue length>`']

Example JSON: 

.. code:: json

    {"queue length": 0}

.. _images processed:

images processed
--------------------

:Type:
  integer
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`images processed <images processed>`']

Example JSON: 

.. code:: json

    {"images processed": 0}

.. _time interval:

time interval
--------------------

:Type:
  number
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`time interval <time interval>`']

Example JSON: 

.. code:: json

    {"time interval": 0}

.. _frames per sec:

frames per sec
--------------------

:Type:
  number
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`frames per sec <frames per sec>`']

Example JSON: 

.. code:: json

    {"frames per sec": 0}

.. _pics:

pics
--------------------

:Type:
  integer
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`pics <pics>`']

Example JSON: 

.. code:: json

    {"pics": 0}

.. _filename:

filename
--------------------

:Type:
  string
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`filename <filename>`']

Example JSON: 

.. code:: json

    {"filename": ""}

.. _array:

array
--------------------

:Type:
  array() items: array 
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`array <array>`']

Example JSON: 

.. code:: json

    {"array": null}

