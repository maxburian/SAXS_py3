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

Consider this excerpt of the ``schema.json``:

.. code:: json

   {
   "type": "object",
   "$schema": "http://json-schema.org/draft-03/schema",
   "required": true,
   "description": "The SAXS configuration file specifies the parameters of a SAXS sensor calibration. It is written in the JSON format which governs the general syntax.",
   "additionalProperties": false,
   "properties": 
      {
         "Directory": 
         {
            "type": "array",
            "required": true,
            "minItems": 1,
            "items": 
            {
               "type": "string",
               "default": ".",
               "appinfo": 
               {
                  "editor": "RemoteDir"
               }
            }
         }
      }
    }


The ``type`` in the root says object which means it is a dictionary like datastructure. 
The possible keys are declared in the ``properties`` doctionary/object. Inside the ``properties``
other nested types are declared in this case an ``array`` called ``Directory``.

The ``appinfo`` section is not part of the Schema specification it is rather a custom field to tell the 
apps who process the schema about possible pecial treatments. In this case we want the Leash use 
Editor widgets
to pick a remote directory. This editor widget will be provided by the QItemDelegate.

The QItemDelegate
-----------------

The QtGui.QTreeView() class allows to set an item delegate this happens for example in ``calibeditor.py``

.. code::

   self.treeview.setItemDelegateForColumn(1,calibeditdelegate.calibEditDelegate( app ))

The calibeditdelegate.calibEditDelegate class in turn is a custom class derived from QtGui.QItemDelegate.
this is implemented in ``calibeditdelegate.py``.

The constructor is only initializing the base class:

.. code::

   class calibEditDelegate(QtGui.QItemDelegate):
       def __init__(self,app,  parent=None):
           super(calibEditDelegate, self).__init__(parent)
           self.app=app
           
The part that is interesting is the reimplementations of the ``createEditor``, 
``commitAndCloseEditor``, ``setEditorData`` and ``setModelData`` methods.


The ``createEditor`` method is called when the user doubleclicks an item content cell in the tree view.
The default behaviour is just to make the text content editable but you can return any widget you like depending 
on the context. 

.. code::


    def createEditor(self, parent, option, index):
        """
        special method of QItemDelegate class
        """
        try:
            subschema=json.loads(unicode(index.model().data(index,role=im.SUBSCHEMA).toString()))
        except ValueError:
            return None
            
        type= unicode(index.model().data(index,role=im.TYPE).toString())
        editablearray= unicode(index.model().data(index,role=im.ISEDITABLEARRAY).toString())
        editortype=None
        if subschema.get("appinfo"):
            editortype= subschema.get("appinfo").get("editor")
    
        print type
        if "enum" in subschema:
            isenum="true"
            enum=subschema['enum']
        else:
            isenum="false"
        
        if type == "integer":
            spinbox = QtGui.QSpinBox(parent)
            spinbox.setRange(-200000, 200000)
            spinbox.setSingleStep(1) 
            spinbox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            return spinbox
        elif type == "number":
            spinbox = QtGui.QDoubleSpinBox(parent)
            spinbox.setRange(-200000, 200000)
            spinbox.setSingleStep(0.1)
            spinbox.setDecimals(4)
            spinbox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            return spinbox
        elif editablearray=="editablearray":
            arrayeditdialog=arrayediddialog(index,parent)
            return arrayeditdialog
        elif  type== "object" or type=="array" or type=="arrayitem" :
            return None
        elif isenum=="true":
            combobox = QtGui.QComboBox(parent)
            combobox.addItems(sorted( enum))
            return combobox
        elif editortype=="File":
            dirname= os.path.dirname(unicode(index.model().filename))
            filepicker=QtGui.QFileDialog(directory=dirname)
            filepicker.setMinimumSize(800,500)
            filepicker.setFileMode(filepicker.ExistingFile)
            return filepicker
        elif editortype=="RemoteDir":
            return RemoteDirPicker(self.app,parent,index)
        elif editortype=="RemoteFile":
            return RemoteDirPicker(self.app,parent,index,showfiles=True)
        else:
            return QtGui.QItemDelegate.createEditor(self, parent, option,
                                              index)
The ``createEditor`` is called with an index object. Which is a class that is used by the 
QtGui.QStandardItemModel class to represent the data in a form the Treeview can display it. 

In the implementation in ``jsonschematreemodel.py`` the items have the subschema describing 
themselved and their children stored in special data attributes. So we can use this to chose which 
editor to present the user depending of the type and role of the item on hand. 
Integers get a QtGui.QSpinBox, Enumerations get  QtGui.QComboBox to select one of the options.

In case the item has ``File`` in the appinfo/editor field,

.. code:: json
   
   { 
      "MaskFile": 
      {
         "description": "Path of Maskfile",
         "type": "string",
         "default": "AAA_integ.msk",
         "required": true,
         "appinfo": 
         {
            "editor": "File",
            "display": "MaskFile"
         }
      }
   }
   
doubleclicking the cell will give the user a file system dialog to select a local file.

The ``"display": "MaskFile"`` field will cause another method to execute custom behaviour. 
The ``setModelData`` method. In this case it will load the mask file and display the picture
 in another cell in the treeview.


