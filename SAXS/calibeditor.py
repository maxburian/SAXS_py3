from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
 
import json
import calibtreemodel
import calibeditdelegate
class calibeditor(QtGui.QWidget):
    def __init__(self,app):
         super(calibeditor,self).__init__( )
         self.app=app
         self.setLayout(QtGui.QVBoxLayout())
         self.treeview=QtGui.QTreeView()
         self.layout().addWidget(self.treeview)
         self.model=calibtreemodel.calibtreemodel(app )
         self.treeview.setModel(self.model)
         self.treeview.setMinimumWidth(800)
         self.treeview.setMinimumHeight(800)
      
         self.treeview.setAlternatingRowColors(True)
         self.treeview.setItemDelegateForColumn(1,calibeditdelegate.calibEditDelegate( app ))
         self.reset()
        
             
         QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"),self,self.model.save)
    def reset(self):
        self.model.invisibleRootItem().setColumnCount(3)
        self.treeview.setColumnWidth(0,320)
        self.treeview.setColumnWidth(1,320)
        self.treeview.expandAll()