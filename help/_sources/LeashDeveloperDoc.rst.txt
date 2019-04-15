===============================
SAXSDOG Developer Documentation
===============================

The Leash
=========

The Leash GUI is part of the SAXSdog Network and the most user facing software. Its design allows to extend it with functionality by touching only small well defined parts. One is the Schemas of the configuration files and the other is the  ``QItemDelegate``. The following sections give an overview of the important parts.

Using the JSON Schema to Extend Leash
-------------------------------------

This software relies a lot on structured configuration files that have to constantly be checked for validity. This is done by defining the grammar in JSON Schema. This is a language, in its self expressed in JSON, made to specify what values may occur where in the file. This does not only allow for automatically generating documentation, as it is used in this document many times, but you can also use it to generate an GUI that can edit this structured data files. 

The tree view in the "Calib" tab of ``Leash`` is build by recursively, going to the schema and the data, building the model that can be displayed in the QtreeView widget.

So, in order to add new parameters to the view, the only thing you must do, is to add the description to the schema. If you use similar constructs as in the rest of the data, it will work just so. 

The leash uses the scheme in ``SAXS/schema.json`` to build the "Calib" tab and 
``SAXS/DataConsolidationConf.json`` to build the Consolidate tab.

Consider this excerpt of the ``SAXS/schema.json``:

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
            "description":"Directory to take into acount for processing images. Given as a list of subdirectories.",
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


The ``type`` in the root says ``object`` which means it is a dictionary like data structure. The possible keys are declared in the ``properties`` dictionary. Inside the ``properties`` other nested types are declared in this case an ``array`` called ``Directory``.

The ``appinfo`` section is not part of the schema specification it is rather a custom field to tell the application  about possible special treatments. In this case we want the Leash use editor widgets
to pick a remote directory. This editor widget will be provided by the ``QItemDelegate``. Which shall be explained in the following section.

The QItemDelegate
-----------------

The ``QtGui.QTreeView()`` class allows to set an item delegate. This happens for example in ``calibeditor.py``

.. code::

   self.treeview.setItemDelegateForColumn(1,calibeditdelegate.calibEditDelegate( app ))

The ``calibeditdelegate.calibEditDelegate`` class in turn is a custom class derived from QtGui.QItemDelegate. This is implemented in ``calibeditdelegate.py``.

The constructor is initializing the base class:

.. code::

   class calibEditDelegate(QtGui.QItemDelegate):
       def __init__(self,app,  parent=None):
           super(calibEditDelegate, self).__init__(parent)
           self.app=app
           
The part that is interesting is the reimplementations of the ``createEditor``, 
``commitAndCloseEditor``, ``setEditorData`` and ``setModelData`` methods.


The ``createEditor`` method is called when the user double clicks an item content cell in the tree view. The default behavior is to make the text content editable but you can return any widget you like, depending on the context. 

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
The ``createEditor`` is called with an index object. Which is a class that is used by the ``QtGui.QStandardItemModel`` class to represent the data in a form the tree view can display it. 

In the implementation in ``jsonschematreemodel.py`` the items have the subschema describing themselves and their children stored in special data attributes. We can use this to chose which editor to present to the user, depending of the type and role of the item on hand. Integers get a ``QtGui.QSpinBox``, Enumerations get  ``QtGui.QComboBox`` to select one of the options.

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
   
double clicking the cell will give the user a file system dialog to select a local file. This time we did not get a small widget that fits into the cell, we got a separate dialog. This means it is possible to launch any kind of fancy dialog from here. Think "mask editor", "powder diffraction calibration" anything you like.
 
The ``"display": "MaskFile"`` field will cause another method to execute custom behavior. The ``setModelData`` method. In this case it will load the mask file and display the picture in another cell in the tree view.


The Image Queue
===============

The :py:class:`imagequeue` class manages how and when to integrate images. It is instantiated by the server when you load up a new calibration and start a new queue. Or, alternatively the ``saxsdog`` command line tool will also create an image queue. It takes as argument a list of integration recipes e.g. radial integration or slices. This recipes can be any Python object that knows how to do something with images as long they implement the :py:meth:`integratechi` method with the same API as the others.

In the initialization process, it will create a queue object, which is a very powerful synchronized data structure which can even be accessed by subprocesses. If the server creates it it will also create a process to listen to the Feeder service and push the image paths into the queue of the ``imagequeue`` object.  

For the work to begin the :py:meth:`imagequeue.start`  method needs to be called. This will create the worker subprocesses to consume the images from the queue.

.. code::

    for threadid in range(1,self.options.threads):
        print "start proc [",threadid,"]"
        worker=Process(target=funcworker, args=(self,threadid))
        worker.daemon=True
        self.pool.append(worker)
        worker.start() 


The imagequeue will launch and manage as many workers as configured in the calibration. The workers are in an infinite loop  where they wait until a new image arrives through the queue to decide whether they are configured to work on the directory the images are in. If so they will process the image and push a small report into the history queue. This report includes the time (for the histogram) and the files written.

If the ``readdir`` command is issued to the server, it will call the  :py:meth:`imagequeue.fillqueuewithexistingfiles` method which will fill the queue with all ".tif" files it finds in the configured directory.

.. include:: DataMerge.rst
