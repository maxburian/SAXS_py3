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
  :ref:`cal <cal>`, :ref:`Error <Error>`, :ref:`directory <directory>`, :ref:`mask <mask>`, :ref:`threads <threads>`, :ref:`dircontent <dircontent>`, :ref:`stat <stat>`, :ref:`filename <filename>`, :ref:`array <array>`
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

.. _threads:

threads
--------------------

:Type:
  integer
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`threads <threads>`']

Example JSON: 

.. code:: json

    {"threads": 0}

.. _dircontent:

dircontent
--------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`dircontent <dircontent>`']

Example JSON: 

.. code:: json

    {"dircontent": {}}

.. _stat:

stat
--------------------

:type:
  object


:Contains:
  :ref:`queue length <queue length>`, :ref:`images processed <images processed>`, :ref:`time <time>`, :ref:`start time <start time>`
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

.. _time:

time
--------------------

:Type:
  number
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`time <time>`']

Example JSON: 

.. code:: json

    {"time": 0}

.. _start time:

start time
--------------------

:Type:
  number
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`start time <start time>`']

Example JSON: 

.. code:: json

    {"start time": 0}

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

