from PyQt4 import  QtGui
from PyQt4 import  QtCore
import json,os,collections
import jsonschematreemodel
import calibeditdelegate
import schematools

class consolidatepanel(QtGui.QWidget):
    def __init__(self,app):
        super(consolidatepanel,self).__init__( )
        self.app=app
        self.hlayout=QtGui.QHBoxLayout()
        self.setLayout(self.hlayout)
        self.treeview=QtGui.QTreeView()
        self.hlayout.addWidget(self.treeview)
        
        self.model=jsonschematreemodel.jsonschematreemodel( app,
                        schema=json.load(open(os.path.dirname(__file__)
                        +os.sep+'DataConsolidationConf.json'),
                        object_pairs_hook=collections.OrderedDict) 
                                                           )
        self.treeview.setModel(self.model)
        self.treeview.setMinimumWidth(800)
        self.treeview.setMinimumHeight(800)
        self.treeview.setAlternatingRowColors(True)
        self.treeview.setItemDelegateForColumn(1,calibeditdelegate.calibEditDelegate( app ))
        self.reset()
        default= schematools.schematodefault( self.model.schema)
        self.filename=os.path.dirname(__file__)   +os.sep+'consolconftemplate.json'
       
        self.model.loadfile(self.filename)
        self.app.calibeditor.reset()
        self.connect(self.model, QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'),self.model.save)
        self.submitbutton=QtGui.QPushButton("Collect All Data")
        self.submitlayout=QtGui.QVBoxLayout()
        self.hlayout.addLayout(self.submitlayout)
        self.submitlayout.addWidget(   self.submitbutton)
        self.submitlayout.addStretch()
    def reset(self):
        self.model.invisibleRootItem().setColumnCount(3)
        self.treeview.setColumnWidth(0,320)
        self.treeview.setColumnWidth(1,320)
        self.treeview.expandAll()