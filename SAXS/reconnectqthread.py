from PyQt4.QtCore import *
from PyQt4.QtGui import  *
import json,os
from Leash import initcommand
import SAXS
class reconnecthread(QThread):
    def __init__(self,mw):
        QThread.__init__(self)
        self.mw=mw
    def run(self):
        try:
            conf=json.load(open(os.path.expanduser("~"+os.sep+".saxdognetwork")))
        except IOError as e:
            self.emit( SIGNAL('error(QString)'),"IOError: Cannot open:"+os.path.expanduser("~"+os.sep+".saxdognetwork")+" "+e.message )
            return
        except ValueError as e:
            self.emit( SIGNAL('error(QString)'),"IOError: Cannot open:"+os.path.expanduser("~"+os.sep+".saxdognetwork")+". Wrong syntax?"+e.message )
            return
        argu=["get"]
        o=SAXS.AttrDict({"server":""})
        result=initcommand(o,argu,conf)
        self.emit( SIGNAL('connected(QString)') ,result)

           