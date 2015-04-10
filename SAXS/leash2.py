
from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
import sys,os
import connectdialog
import calibeditor
import leashmenue
import Leash
import json
from jsonschema import validate,ValidationError
import plotdatathread
import plotpanel
import histpanel
import checkServerCalibchanged
import collections
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
        self.appdir=os.path.dirname(__file__)+os.sep
        self.mainWindow.setWindowIcon(QtGui.QIcon(self.appdir+"icons"+os.sep+"program.png"))
        self.tab=QtGui.QTabWidget()
        self.calib=QtGui.QWidget()
        self.caliblayout=QtGui.QHBoxLayout()
        self.calib.setLayout(self.caliblayout)
        self.calibeditor=calibeditor.calibeditor(self)
        self.caliblayout.addWidget(self.calibeditor)
        self.submitlayout=QtGui.QVBoxLayout()
        self.caliblayout.addLayout(self.submitlayout)
        self.queuestatuslabel=QtGui.QLabel("No queue on server.")
        self.filestatuslabel=QtGui.QLabel("")
        self.submitbutton=QtGui.QPushButton("Start Server Queue")
        self.submitlayout.addWidget(self.queuestatuslabel)
        self.submitlayout.addWidget( self.filestatuslabel)
        self.submitlayout.addWidget(self.submitbutton)
        self.submitlayout.addStretch()
        self.tab.addTab( self.calib , "Calib")
        self.plotplanel=plotpanel.plotpanel()
        self.tab.addTab( self.plotplanel , "Plots")
        self.histpanel=histpanel.histpanel(self)
        self.tab.addTab( self.histpanel , "History")
        self.mainWindow.setCentralWidget (self.tab  )
        self.connect(self.submitbutton,QtCore.SIGNAL('clicked()'),self.startqueue)
        self.connect(self.calibeditor.model,QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"),self.statusmodified)
        self.errormessage=QtGui.QErrorMessage()
        self.menue=leashmenue.menueitems(self)
        self.connect(self.calibeditor.model, QtCore.SIGNAL("fileNameChanged()"),self.updatewindowtitle)
        self.plotthread=plotdatathread.plotthread(self)
        self.connect(self.plotthread,QtCore.SIGNAL("plotdata(QString)"),self.plotplanel.plot)
        self.connect(self.plotthread,QtCore.SIGNAL("plotdata(QString)"),self.histpanel.plot)
        self.connect(self.plotthread,QtCore.SIGNAL("histupdate(QString)"),self.histpanel.timestep)
      
        self.checkServerCalibchanged=checkServerCalibchanged.checkServerCalibChangedThread(self)
        self.connect(self.plotthread,QtCore.SIGNAL("ServerQueueTimeChanged()"),  self.checkServerCalibchanged.start)
        self.connect(self.checkServerCalibchanged,QtCore.SIGNAL("ServerQueueChanged(QString)"),self.notifyServerChange)
        if   reconnectresult["result"]=="cal":
            self.calibeditor.model.loadservercalib(reconnectresult)
            self.calibeditor.reset()
            self.mainWindow.setWindowTitle("SAXS Leash: Server Calibration")
            self.setqueuesynced()
           
        elif len(self.args)>0:
            filename=self.args[0]
            self.calibeditor.model.loadfile(filename)
            self.calibeditor.reset()
            self.mainWindow.setWindowTitle("SAXS Leash: "+filename)
            self.menue.appendrecentfile(filename)
        
        self.plotthread.start()
        
    def parscecommandline(self):
      
        self.options,self.args= Leash.parsecommandline()
    def startqueue(self):
        data=self.calibeditor.model.getjson()
        self.calibeditor.model.save()
        argu=["new", data]
        result={}
        try:
            result=json.loads(Leash.initcommand(self.options,argu,self.netconf))
        except Exception as e:
            self.errormessage.setWindowTitle("Server Error")
            self.errormessage.setMinimumSize(400, 300)
            self.errormessage.showMessage( str(e))
        if 'result' in result and result['result']=="new queue":
            print result
            self.setqueuesynced()
            self.plotthread.start()
        else:
            self.errormessage.setWindowTitle("Server Error")
            self.errormessage.setMinimumSize(400, 300)
            self.errormessage.showMessage(json.dumps(result,indent=2))
    def setqueuesynced(self):
        self.queuestatuslabel.setText("Queue started.")
        self.filestatuslabel.setText("Local calibration synced")
        if self.calibeditor.model.filename:
            self.mainWindow.setWindowTitle("SAXS Leash: "+self.calibeditor.model.filename)
        else:
            self.mainWindow.setWindowTitle("SAXS Leash: Servercalibration")
    def statusmodified(self):
        self.filestatuslabel.setText ("Local calibration modified.")
        if self.calibeditor.model.filename:
            self.mainWindow.setWindowTitle("SAXS Leash: "+self.calibeditor.model.filename)
        else:
            self.mainWindow.setWindowTitle("SAXS Leash: Servercalibration")
    def updatewindowtitle(self):
        self.mainWindow.setWindowTitle("SAXS Leash: "+self.calibeditor.model.filename)
    def notifyServerChange(self,serverdata):
        message =QtGui.QMessageBox()
        message.setText("The Server Calibration Changed")
        message.setInformativeText("Do you want to load the new Calibration from the server")
        message.setStandardButtons( message.Cancel)
        Okbutton=message.addButton( "Load", message.AcceptRole)
        result=message.exec_()
       
        if result==0:
              ServerData=json.loads(unicode(serverdata),object_pairs_hook=collections.OrderedDict)
              self.calibeditor.model.loadservercalib(ServerData)
              self.calibeditor.reset()
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