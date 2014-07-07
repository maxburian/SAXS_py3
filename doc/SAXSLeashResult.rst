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
  :ref:`result <result>`, :ref:`data <data>`
:Required:
  True
:JSON Path:
  :ref:`# <root>` 

Example JSON: 

.. code:: json

    {}

.. _result:

result
--------------------

:Type:
  string
:Required:
  False
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
  :ref:`queue length <queue length>`, :ref:`images processed <images processed>`, :ref:`queue id <queue id>`, :ref:`file name <file name>`, :ref:`header <header>`, :ref:`array <array>`
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`']

Example JSON: 

.. code:: json

    {"data": {}}

.. _queue length:

queue length
--------------------

:Type:
  integer
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`queue length <queue length>`']

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
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`images processed <images processed>`']

Example JSON: 

.. code:: json

    {"images processed": 0}

.. _queue id:

queue id
--------------------

:Type:
  string
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`queue id <queue id>`']

Example JSON: 

.. code:: json

    {"queue id": ""}

.. _file name:

file name
--------------------

:Type:
  string
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`file name <file name>`']

Example JSON: 

.. code:: json

    {"file name": ""}

.. _header:

header
--------------------

:Type:
  array() items: string 
:Required:
  False
:JSON Path:
  :ref:`# <root>` [':ref:`data <data>`'][':ref:`header <header>`']

Example JSON: 

.. code:: json

    {"header": null}

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

