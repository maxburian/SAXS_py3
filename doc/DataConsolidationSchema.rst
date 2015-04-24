.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

.. _required:

 The ':red:`*`' signifies a required Field.

:Type:
  object
:Contains:
  :ref:`TimeOffset <TimeOffset>`:red:`*`, :ref:`LogDataTables <LogDataTables>`, :ref:`OutputFormats <OutputFormats>`:red:`*`, :ref:`OutputFileBaseName <OutputFileBaseName>`:red:`*`, :ref:`HDFOptions <HDFOptions>`:red:`*`
:Required:
  False
:JSON Path:
  * :ref:`# <consroot>` 

Example JSON: 

.. code:: json

    {
      "TimeOffset": "0",
      "HDFOptions": {
        "IncludeCHI": false,
        "IncludeTIF": false
      },
      "OutputFormats": {
        "exel": false,
        "hdf": false,
        "json": false,
        "csv": false
      },
      "OutputFileBaseName": "../results/merged"
    }

.. _TimeOffset:

TimeOffset
-------------------------

If offset is not found otherwise, use this as offset  for all log data


:Type:
  number in Seconds
:Required:
  True
:Default:
  0
:JSON Path:
  * :ref:`# <consroot>` [':ref:`TimeOffset <TimeOffset>`']

Example JSON: 

.. code:: json

    {"TimeOffset": "0"}

.. _LogDataTables:

LogDataTables
-------------------------

Define log files to consolidate with image data. If more then one defined, they will be joined and missing values will be interpolated.


:Type:
  array() items: {:ref:`TimeEpoch`, :ref:`TimeOffset`, :ref:`FirstImageCorrelation`, :ref:`Name`, :ref:`Files`}
:Required:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`LogDataTables <LogDataTables>`']

Example JSON: 

.. code:: json

    {"LogDataTables": []}

.. _TimeEpoch:

TimeEpoch
-------------------------

Time epoch


:Type:
  string
:values:
  [Mac,Unix]

:Required:
  True
:Default:
  Mac
:JSON Path:
  * :ref:`# <consroot>` [':ref:`LogDataTables <LogDataTables>`'][0][':ref:`TimeEpoch <TimeEpoch>`']

Example JSON: 

.. code:: json

    {"TimeEpoch": "Mac"}

.. _TimeOffset:

TimeOffset
-------------------------

If offset is not found otherwise, use this as offset.


:Type:
  number in Seconds
:Required:
  True
:Default:
  0
:JSON Path:
  * :ref:`# <consroot>` [':ref:`LogDataTables <LogDataTables>`'][0][':ref:`TimeOffset <TimeOffset>`']

Example JSON: 

.. code:: json

    {"TimeOffset": "0"}

.. _FirstImageCorrelation:

FirstImageCorrelation
-------------------------

Find offset for all log data by correlating first image with first entry of this table. 


:Type:
  boolean
:Required:
  True
:Default:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`LogDataTables <LogDataTables>`'][0][':ref:`FirstImageCorrelation <FirstImageCorrelation>`']

Example JSON: 

.. code:: json

    {"FirstImageCorrelation": false}

.. _Name:

Name
-------------------------

Name field to be used as prefix in the joined collumn names.


:Type:
  string
:Required:
  True
:Default:
  log
:JSON Path:
  * :ref:`# <consroot>` [':ref:`LogDataTables <LogDataTables>`'][0][':ref:`Name <Name>`']

Example JSON: 

.. code:: json

    {"Name": "log"}

.. _Files:

Files
-------------------------

One log table may be one file, or a list of files to be concatenated.


:Type:
  array() items: {:ref:`RemotePath`, :ref:`LocalPath`}
:Required:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`LogDataTables <LogDataTables>`'][0][':ref:`Files <Files>`']

Example JSON: 

.. code:: json

    {"Files": []}

.. _RemotePath:

RemotePath
-------------------------

Path of logfile on server if used in server mode.


:Type:
  array() items: string 
:Required:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`LogDataTables <LogDataTables>`'][0][':ref:`Files <Files>`'][0][':ref:`RemotePath <RemotePath>`']

Example JSON: 

.. code:: json

    {"RemotePath": []}

.. _LocalPath:

LocalPath
-------------------------

Path of logfile on client. Overrides 'RemotePath'.


:Type:
  string
:Required:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`LogDataTables <LogDataTables>`'][0][':ref:`Files <Files>`'][0][':ref:`LocalPath <LocalPath>`']

Example JSON: 

.. code:: json

    {"LocalPath": ""}

.. _OutputFormats:

OutputFormats
-------------------------

List of outputformats to write the consolidated log or the consolidated 'hdf' file.


:Type:
  object
:Contains:
  :ref:`csv <csv>`:red:`*`, :ref:`hdf <hdf>`:red:`*`, :ref:`exel <exel>`:red:`*`, :ref:`json <json>`:red:`*`
:Required:
  True
:JSON Path:
  * :ref:`# <consroot>` [':ref:`OutputFormats <OutputFormats>`']

Example JSON: 

.. code:: json

    {
      "OutputFormats": {
        "exel": false,
        "hdf": false,
        "json": false,
        "csv": false
      }
    }

.. _csv:

csv
-------------------------

:Type:
  boolean
:Required:
  True
:Default:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`OutputFormats <OutputFormats>`'][':ref:`csv <csv>`']

Example JSON: 

.. code:: json

    {"csv": false}

.. _hdf:

hdf
-------------------------

:Type:
  boolean
:Required:
  True
:Default:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`OutputFormats <OutputFormats>`'][':ref:`hdf <hdf>`']

Example JSON: 

.. code:: json

    {"hdf": false}

.. _exel:

exel
-------------------------

:Type:
  boolean
:Required:
  True
:Default:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`OutputFormats <OutputFormats>`'][':ref:`exel <exel>`']

Example JSON: 

.. code:: json

    {"exel": false}

.. _json:

json
-------------------------

:Type:
  boolean
:Required:
  True
:Default:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`OutputFormats <OutputFormats>`'][':ref:`json <json>`']

Example JSON: 

.. code:: json

    {"json": false}

.. _OutputFileBaseName:

OutputFileBaseName
-------------------------

:Type:
  string
:Required:
  True
:Default:
  ../results/merged
:JSON Path:
  * :ref:`# <consroot>` [':ref:`OutputFileBaseName <OutputFileBaseName>`']

Example JSON: 

.. code:: json

    {"OutputFileBaseName": "../results/merged"}

.. _HDFOptions:

HDFOptions
-------------------------

Options only relevant to hdf export.


:Type:
  object
:Contains:
  :ref:`IncludeCHI <IncludeCHI>`:red:`*`, :ref:`IncludeTIF <IncludeTIF>`:red:`*`
:Required:
  True
:JSON Path:
  * :ref:`# <consroot>` [':ref:`HDFOptions <HDFOptions>`']

Example JSON: 

.. code:: json

    {"HDFOptions": {"IncludeCHI": false,"IncludeTIF": false}}

.. _IncludeCHI:

IncludeCHI
-------------------------

Whether to include the .chi files as strings.


:Type:
  boolean
:Required:
  True
:Default:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`HDFOptions <HDFOptions>`'][':ref:`IncludeCHI <IncludeCHI>`']

Example JSON: 

.. code:: json

    {"IncludeCHI": false}

.. _IncludeTIF:

IncludeTIF
-------------------------

Whether to include the images as integer array.


:Type:
  boolean
:Required:
  True
:Default:
  False
:JSON Path:
  * :ref:`# <consroot>` [':ref:`HDFOptions <HDFOptions>`'][':ref:`IncludeTIF <IncludeTIF>`']

Example JSON: 

.. code:: json

    {"IncludeTIF": false}

