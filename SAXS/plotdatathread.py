import json,os
import atrdict
import numpy as np
from Leash import initcommand
import time
from PyQt4 import  QtGui
from PyQt4 import  QtCore
class plotthread(QtCore.QThread):
    def __init__(self,app):
         super(plotthread, self).__init__()
         self.app=app
         self.lastcount=0
    def run(self):
        while True:
            result=json.loads(initcommand(self.app.options,["stat"],self.app.netconf))
            time.sleep(1)
            if result['data']["stat"]['images processed']!=self.lastcount:
                self.lastcount=result['data']["stat"]['images processed']
                plotdata=result=initcommand(self.app.options,["plotdata"],self.app.netconf)
                self.emit(QtCore.SIGNAL('plotdata(QString)'), plotdata)
            else:
                 self.emit(QtCore.SIGNAL('histupdate()'))
            