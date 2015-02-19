from PyQt4.QtCore import *
from PyQt4.QtGui import  *
import json,os
from Leash import initcommand
import atrdict
class reconnecthread(QThread):
    """
    this thread handles reconnection at startup and timeout
    """
    def __init__(self  ,conf):
        QThread.__init__(self)
     
        self.conf=conf
    def run(self):
   
        argu=["get"]
        opt=atrdict.AttrDict({"serverno":None,"server":self.conf["Server"]})
        result=initcommand( opt,argu,self.conf )
        self.emit( SIGNAL('connected(QString)') ,result)

           