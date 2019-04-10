from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
from . import reconnectqthread
import json


class serverstatus(QtGui.QWidget):
    def __init__(self, layout, config, index):
        super(serverstatus, self).__init__( )
        self.layout=layout
        self.index=index
        self.layout.addWidget(QtGui.QLabel( config['Name']+":\n"+config['Server']))
        self.status=QtGui.QLabel("Offline")
        self.layout.addWidget(self.status) 
        self.result=None
        self.connectthread=reconnectqthread.reconnecthread(config)
        self.connect(self.connectthread, QtCore.SIGNAL('connected(QString)'), self.updatestatus)
        self.connectthread.start()
      
    def updatestatus(self, message):
        result=json.loads(str(message))
        self.status.setText("Online, " +result['result'])
        self.result=result
        if result["result"]!="AuthenticationError":
            self.accept=QtGui.QPushButton("Take This")
            self.layout.addWidget(self.accept)
            self.connect(self.accept, QtCore.SIGNAL("clicked()"), self.emitservernumber)
    def emitservernumber(self):
        self.emit(QtCore.SIGNAL('selected(int )'), self.index)
       
class connectdialog(QtGui.QDialog):
    def __init__(self, confs, app):
         super(connectdialog, self).__init__(  )
         self.setWindowTitle("Connect Leash")
         self.vlayout=QtGui.QVBoxLayout()
         self.setLayout(self.vlayout)
         self.vlayout.addWidget(QtGui.QLabel("You have "+str(len(confs))+" Servers configured:"))
         self.serverstatus=[]
         self.confindex=0
         self.ok=False
         self.app=app
         self.setModal(True)
         self.confs=confs
         for index, conf in enumerate(confs):
             hlayout1=QtGui.QHBoxLayout()
             self.vlayout.addLayout(hlayout1)
             self.serverstatus.append(serverstatus(hlayout1, conf, index))
             self.connect(self.serverstatus[index], QtCore.SIGNAL("selected(int )"), self.selected)
             self.connect(self.serverstatus[index], QtCore.SIGNAL("serverselected(int )"), lambda x:x)
         self.startlocalbutton=QtGui.QPushButton("Start Local Server")
         self.vlayout.addWidget(self.startlocalbutton)
         self.connect( self.startlocalbutton, QtCore.SIGNAL("clicked()"), self.startlocalserver)
    def selected(self, index):
        self.confindex=index
        self.accept()
        self.ok=True
    def getval(self):
        for index in len(confs):
            self.onlineconfs[index] = self.serverstatus[index].online
        return self.confindex
    def startlocalserver(self):
        self.confindex=-1
        self.accept()
        self.ok=True
        print("OK")
        self.confs.append( {
                            "Secret": "bd79955f7f17dc390a97df6d747a97",
                            "Server": "tcp://localhost:9945",
                            "Name": "Local",
                            "Feeder": "tcp://localhost:9823"
                           })
       
         