========================================
SAXSDOG Network  Developer Documentation
========================================

The Leash
=========

The Leash GUI is part of the SAXSdog Network and the most user facing software.
It is also the most complex one. There is however the possibillity to extend it with functionality
by touching only small well defined parts. One is the Schemas of the configuration files and the other
is the  QItemDelegate class that controlls how configuration data is shown and edited.

Using the JSON Schema to extend Leash
-------------------------------------

This SAXS package relies in many locations on structured configuration files or protokol data that has 
constantly be checked for validity. This is done by defining the grammar in JSON Schema. This is a language in
itsself expressed in JSON to specify what values may occure wher in the file. This does not only allow for
automatically generating documentation as it is used in this document many times, but you can also use it 
to generate an GUI that can edit this structured data files. 

The treview in the "Calib" tab is build by recursively, going to the schema and the data, and so, 
buiding the model that can be displayed in the QtreeViev widget of the QT tool kit.

So, in order to add new parameteres to the view, the only thing you must do is to add the description to the 
schema. If you use similar constructs as in the rest of the data it will work just so. 

The leash uses the scheme in ``SAXS/schema.json`` to build the "Calib" tab and 
``SAXS/DataConsolidationConf.json`` to build the Consolidate tab.
