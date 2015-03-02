
from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
import sys,os
import connectdialog
import calibeditor
import Leash
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
        selected=self.connectdialog.confindex
        if  self.connectdialog.ok:
            reconnectresult=self.connectdialog.serverstatus[selected].result
        else:
            sys.exit()
        self.netconf=self.confs[selected]
        self.parscecommandline()
        self.loadui(reconnectresult)
    def loadui(self,reconnectresult):
        
        self.mainWindow=super(LeashUI,self)
        self.mainWindow.setWindowTitle("SAXS Leash")
        self.tab=QtGui.QTabWidget()
        self.calib=QtGui.QWidget()
        self.caliblayout=QtGui.QHBoxLayout()
        self.calib.setLayout(self.caliblayout)
        self.calibeditor=calibeditor.calibeditor(self)
        self.caliblayout.addWidget(self.calibeditor)
        self.submitlayout=QtGui.QVBoxLayout()
        self.caliblayout.addLayout(self.submitlayout)
        self.statuslabel=QtGui.QLabel("No queue on server.")
        self.submitbutton=QtGui.QPushButton("Start Server Queue")
        self.submitlayout.addWidget(self.statuslabel)
        self.submitlayout.addWidget(self.submitbutton)
        self.submitlayout.addStretch()
        
        self.tab.addTab( self.calib , "Calib")
        self.mainWindow.setCentralWidget (self.tab  )
        self.connect(self.submitbutton,QtCore.SIGNAL('clicked()'),self.startqueue)
       
        if   reconnectresult["result"]=="cal":
            self.calibeditor.model.loadservercalib(reconnectresult)
            self.calibeditor.reset()
            self.mainWindow.setWindowTitle("SAXS Leash: Server Calibration")
        elif len(self.args)>0:
            filename=self.args[0]
            self.calibeditor.model.loadfile(filename)
            self.calibeditor.reset()
            self.mainWindow.setWindowTitle("SAXS Leash: "+filename)
    def parscecommandline(self):
      
        self.options,self.args= Leash.parsecommandline()
    def startqueue(self):
        data=self.calibeditor.model.getjson()
        argu=["new", data]
        result=Leash.initcommand(self.options,argu,self.netconf)
        print result
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