import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from lablistitems import Lablistitems
__version__ = "1.0.0"
class MainWindow(QMainWindow):
    def __init__(self,app,parent=None):
        super(MainWindow,self).__init__(parent)
        self.ui=uic.loadUi(os.path.dirname(__file__)+os.sep+"lablist.ui",self)
        self.mainWindow=super(MainWindow,self)
        self.mainWindow.setWindowTitle("SAXS Lab List")
        self.listlayout= self.ui.verticalLayout
        self.listmanager=Lablistitems(self.listlayout)
        
 

def GUI():
    app=QApplication(sys.argv)

    form=MainWindow(app)
    form.show()
    app.exec_()
if __name__ == "__main__":
    GUI()