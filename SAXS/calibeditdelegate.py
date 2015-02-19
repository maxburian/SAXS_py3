from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
 
import json

class calibEditDelegate(QtGui.QItemDelegate):
    def __init__(self,  parent=None):
        super(calibEditDelegate, self).__init__(parent)