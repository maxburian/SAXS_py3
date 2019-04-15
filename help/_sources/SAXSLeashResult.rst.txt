.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

.. _required:

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
-------------------------

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
-------------------------

:Type:
  object
:Contains:
  :ref:`cal <cal>`, :ref:`Error <Error>`, :ref:`syncplot <syncplot>`, :ref:`directory <directory>`, :ref:`attachments <attachments>`, :ref:`threads <threads>`, :ref:`dircontent <dircontent>`, :ref:`history <history>`, :ref:`fileslist <fileslist>`, :ref:`stat <stat>`, :ref:`filename <filename>`, :ref:`IntegralParameters <IntegralParameters>`, :ref:`graphs <graphs>`
:Required:
  True
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`']

Example JSON: 

.. code:: json

    {"data": {}}

.. _cal:

cal
-------------------------

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
-------------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`Error <Error>`']

Example JSON: 

.. code:: json

    {"Error": {}}

.. _syncplot:

syncplot
-------------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`syncplot <syncplot>`']

Example JSON: 

.. code:: json

    {"syncplot": {}}

.. _directory:

directory
-------------------------

Directory this queue is going to use. New files in other directories are going to be ignored.


:Type:
  array() items: 
:Required:
  False
:Default:
  [u'.', u'', u'']
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`directory <directory>`']

Example JSON: 

.. code:: json

    {"directory": [".","",""]}

.. _attachments:

attachments
-------------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`attachments <attachments>`']

Example JSON: 

.. code:: json

    {"attachments": {}}

.. _threads:

threads
-------------------------

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
-------------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`dircontent <dircontent>`']

Example JSON: 

.. code:: json

    {"dircontent": {}}

.. _history:

history
-------------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`history <history>`']

Example JSON: 

.. code:: json

    {"history": {}}

.. _fileslist:

fileslist
-------------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`fileslist <fileslist>`']

Example JSON: 

.. code:: json

    {"fileslist": {}}

.. _stat:

stat
-------------------------

:type:
  object


:Contains:
  :ref:`queue length <queue length>`, :ref:`images processed <images processed>`, :ref:`time <time>`, :ref:`start time <start time>`, :ref:`mergecount <mergecount>`
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`']

Example JSON: 

.. code:: json

    {"stat": {}}

.. _queue length:

queue length
-------------------------

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
-------------------------

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
-------------------------

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
-------------------------

:Type:
  number
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`start time <start time>`']

Example JSON: 

.. code:: json

    {"start time": 0}

.. _mergecount:

mergecount
-------------------------

:Type:
  number
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`stat <stat>`'][':ref:`mergecount <mergecount>`']

Example JSON: 

.. code:: json

    {"mergecount": 0}

.. _filename:

filename
-------------------------

:Type:
  string
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`filename <filename>`']

Example JSON: 

.. code:: json

    {"filename": ""}

.. _IntegralParameters:

IntegralParameters
-------------------------

:type:
  object


:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`IntegralParameters <IntegralParameters>`']

Example JSON: 

.. code:: json

    {"IntegralParameters": {}}

.. _graphs:

graphs
-------------------------

:Type:
  array() items: {:ref:`kind`, :ref:`conf`, :ref:`columnLabels`, :ref:`array`}
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`graphs <graphs>`']

Example JSON: 

.. code:: json

    {"graphs": []}

.. _kind:

kind
-------------------------

:Type:
  string
:values:
  [Radial, Slice]

:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`graphs <graphs>`'][0][':ref:`kind <kind>`']

Example JSON: 

.. code:: json

    {"kind": "Radial"}

.. _conf:

conf
-------------------------

:Type:
  object
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`graphs <graphs>`'][0][':ref:`conf <conf>`']

Example JSON: 

.. code:: json

    {"conf": null}

.. _columnLabels:

columnLabels
-------------------------

:Type:
  array() items: string 
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`graphs <graphs>`'][0][':ref:`columnLabels <columnLabels>`']

Example JSON: 

.. code:: json

    {"columnLabels": []}

.. _array:

array
-------------------------

:Type:
  array() items: 
:Required:
  False
:JSON Path:
  * :ref:`# <resroot>` [':ref:`data <data>`'][':ref:`graphs <graphs>`'][0][':ref:`array <array>`']

Example JSON: 

.. code:: json

    {"array": []}

