from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
 
import json
import calibtreemodel
import calibeditdelegate
class calibeditor(QtGui.QWidget):
    def __init__(self):
     super(calibeditor,self).__init__( )
     self.setLayout(QtGui.QVBoxLayout())
     self.treeview=QtGui.QTreeView()
     self.layout().addWidget(self.treeview)
     self.model=calibtreemodel.calibtreemodel( )
     self.treeview.setModel(self.model)
     self.treeview.setItemDelegateForColumn(1,calibeditdelegate.calibEditDelegate(  ))