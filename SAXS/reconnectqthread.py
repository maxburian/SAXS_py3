from PyQt4.QtCore import *
from PyQt4.QtGui import  *
import json,os
from Leash import initcommand
import atrdict
class reconnecthread(QThread):
    """
    this thread handles reconnection at startup and timeout
    """
    def __init__(self,mw):
        QThread.__init__(self)
        self.mw=mw
    def run(self):
        try:
            conf=json.load(open(os.path.expanduser("~"+os.sep+".saxsdognetwork")))
        except IOError as e:
            self.emit( SIGNAL('error(QString)'),"IOError: Cannot open:"+os.path.expanduser("~"+os.sep+".saxsdognetwork")+" "+e.message )
            return
        except ValueError as e:
            self.emit( SIGNAL('error(QString)'),"IOError: Cannot open:"+os.path.expanduser("~"+os.sep+".saxsdognetwork")+". Wrong syntax?"+e.message )
            return
        argu=["get"]
        o=atrdict.AttrDict({"server":""})
        result=initcommand(self.mw.options,argu,conf)
        self.emit( SIGNAL('connected(QString)') ,result)

           