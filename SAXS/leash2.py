
from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
import sys,os
import connectdialog
import calibeditor
import json
from jsonschema import validate,ValidationError
class LeashUI(QtGui.QMainWindow):
    def __init__(self,app,parent=None):
        super(LeashUI,self).__init__(parent)
        self.clipboard=app.clipboard()
        self.confs=json.load(open(os.path.expanduser("~"+os.sep+".saxsdognetwork")))
        validate( self.confs,json.load(open(os.path.dirname(__file__)+os.sep+'NetworkSchema.json')))
        self.connectdialog=connectdialog.connectdialog( self.confs)
        self.connectdialog.exec_()
        self.parscecommandline()
        self.loadui()
    def loadui(self):
        
        self.mainWindow=super(LeashUI,self)
        self.mainWindow.setWindowTitle("SAXS Leash")
        self.tab=QtGui.QTabWidget()
        self.calib=QtGui.QWidget()
        self.caliblayout=QtGui.QHBoxLayout()
        self.calib.setLayout(self.caliblayout)
        self.calibeditor=calibeditor.calibeditor(self)
        self.caliblayout.addWidget(self.calibeditor)
        self.tab.addTab( self.calib , "Calib")
        self.mainWindow.setCentralWidget (self.tab  )
    def parscecommandline(self):
        import Leash
        self.otions,self.args= Leash.parsecommandline()
    def cleanup(self):
        pass
def LeashGUI():
    
    app=QtGui.QApplication(sys.argv)
    form=LeashUI(app)
    form.show()
    app.exec_()
    form.cleanup()
if __name__ == "__main__":
   
    LeashGUI( )