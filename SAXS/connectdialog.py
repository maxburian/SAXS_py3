from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
import reconnectqthread
import json
class serverstatus(QtGui.QWidget):
    def __init__(self,layout,config,index):
        super(serverstatus,self).__init__( )
        self.layout=layout
        self.index=index
        self.layout.addWidget(QtGui.QLabel( config['Name']+":\n"+config['Server']))
        self.status=QtGui.QLabel("Offline")
        self.layout.addWidget(self.status) 
       
        self.connectthread=reconnectqthread.reconnecthread( config)
        self.connect(self.connectthread,QtCore.SIGNAL('connected(QString)'),self.updatestatus)
        self.connectthread.start()
      
    def updatestatus(self,message):
        result=json.loads(unicode(message))
        
        self.status.setText("Online, " +result['result'])
        self.result=result
        if result["result"]!="AuthenticationError":
            self.accept=QtGui.QPushButton("Take This")
            self.layout.addWidget(self.accept)
            self.connect(self.accept,QtCore.SIGNAL("clicked()"),self.emitservernumber)
    def emitservernumber(self):
        self.emit(QtCore.SIGNAL('selected(int )'),self.index)
       
class connectdialog(QtGui.QDialog):
    def __init__(self,confs):
         super(connectdialog,self).__init__( )
         self.setWindowTitle("Connect Leash")
         self.vlayout=QtGui.QVBoxLayout()
         self.setLayout(self.vlayout)
         self.vlayout.addWidget(QtGui.QLabel("You have "+str(len(confs))+" Servers configured:"))
         self.serverstatus=[]
         self.confindex=0
         self.ok=False
         self.setModal(True)
         for index,conf in enumerate(confs):
             hlayout1=QtGui.QHBoxLayout()
             self.vlayout.addLayout(hlayout1)
             self.serverstatus.append(serverstatus(hlayout1,conf,index))
             self.connect(self.serverstatus[index],QtCore.SIGNAL("selected(int )"),self.selected)
    def selected(self,index):
        self.confindex=index
        self.accept()
        self.ok=True
    def getval(self):
        return self.confindex