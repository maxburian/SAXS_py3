.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

:.. _required:

 The ':red:`*`' signifies a required Field.

Schema for requests from Saxs Leash to Saxs Server


:Type:
  object
:Contains:
  :ref:`result <result>`:red:`*`, :ref:`data <data>`:red:`*`
:Required:
  True
:JSON Path:
  * :ref:`# <resroot>` 

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
  * :ref:`# <resroot>` [':ref:`result <result>`']

Example JSON: 

.. code:: json

    {"result": ""}

.. _data:

data
--------------------

:Type:
  object
:Contains:
  :ref:`cal <cal>`, :ref:`Error <Error>`, :ref:`directory <directory>`, :ref:`mask <mask>`, :ref:`stat <stat>`, :ref:`filename <filename>`, :ref:`array <array>`
:Required:
  True
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`']

Example JSON: 

.. code:: json

    {"data": {}}

.. _cal:

cal
--------------------

:Type:
  object
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`cal <cal>`']

Example JSON: 

.. code:: json

    {"cal": null}

.. _Error:

Error
--------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`Error <Error>`']

Example JSON: 

.. code:: json

    {"Error": {}}

.. _directory:

directory
--------------------

Directory this queue is going to use. New files in other directories are going to be ignored.


:Type:
  array() items: string 
:Required:
  False
:Default:
  [u'.', u'', u'']
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`directory <directory>`']

Example JSON: 

.. code:: json

    {"directory": [".","",""]}

.. _mask:

mask
--------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`mask <mask>`']

Example JSON: 

.. code:: json

    {"mask": {}}

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
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`']

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
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`queue length <queue length>`']

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
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`images processed <images processed>`']

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
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`time interval <time interval>`']

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
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`frames per sec <frames per sec>`']

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
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`pics <pics>`']

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
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`filename <filename>`']

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
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`array <array>`']

Example JSON: 

.. code:: json

    {"array": null}

