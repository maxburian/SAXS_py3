import json,os
from . import atrdict
import numpy as np
from .Leash import initcommand
import time
from PyQt4 import  QtGui
from PyQt4 import  QtCore
class plotthread(QtCore.QThread):
    def __init__(self,app):
         super(plotthread, self).__init__()
         self.app=app
         self.lastcount=0
         self.lastmergecount=0
         self.queuestarttime=None
    def run(self):
        self.queuestarttime=None
       
        while True:
            time.sleep(2)
            resultstr=initcommand(self.app.options,["stat"],self.app.netconf)
            result=json.loads(resultstr)
            if "Error" in result['data']:
                print("Error here")
                continue
            if 'start time' in result['data']["stat"]:
                starttime=result['data']["stat"]['start time']
                if self.queuestarttime and self.queuestarttime!=starttime:
                    self.emit(QtCore.SIGNAL('ServerQueueTimeChanged()'))
            
                self.queuestarttime=starttime
                
            if ( 'images processed' in  result['data']["stat"]):
                fresh=False
                if(result['data']["stat"]['images processed']!=self.lastcount):
                    self.lastcount=result['data']["stat"]['images processed']
                    plotdata=initcommand(self.app.options,["plotdata"],self.app.netconf)
                    self.emit(QtCore.SIGNAL('plotdata(QString)'), plotdata)
                else:
                    self.emit(QtCore.SIGNAL('histupdate(QString)'),resultstr)
            if ( 'mergecount' in  result['data']["stat"]): 
                if(result['data']["stat"]['mergecount']!=self.lastmergecount):
                    self.lastmergecount=result['data']["stat"]['mergecount']
                    mergedata=initcommand(self.app.options,["getmergedata"],self.app.netconf)
                    self.emit(QtCore.SIGNAL('mergeresultdata(QString)'), mergedata)
                    print("getmergedata")
    
            elif result["result"]=="Error":
                self.emit(QtCore.SIGNAL('ProtocolError(QString)'), plotdata)
            