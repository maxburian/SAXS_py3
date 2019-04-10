import numpy as np
from .Leash import initcommand
import time
from PyQt4 import  QtGui
from PyQt4 import  QtCore
import base64
import json
import hashlib
 
class checkServerCalibChangedThread(QtCore.QThread):
    def __init__(self, app):
         super(checkServerCalibChangedThread, self).__init__()
         self.app=app
       
        
    def run(self):
          print("############Check Server Calib"+ str(self.app.netconf))
          ServerCalib=json.loads(initcommand(self.app.options, ["get"], self.app.netconf))
          LocalCalib=json.loads(json.dumps(self.app.calibeditor.model.getjson()))
          json.dump(ServerCalib["data"], open("server", "w"), indent=2, sort_keys=True)#
          json.dump(LocalCalib, open("local", "w"), indent=2, sort_keys=True)
          hash1=hashlib.sha1()
          hash2=hashlib.sha1()
          hash1.update(json.dumps(ServerCalib["data"]["cal"], sort_keys=True).encode('utf-8'))
          hash2.update(json.dumps(LocalCalib, sort_keys=True).encode('utf-8'))
          # hash attachments
          if True:
              for attachment in ServerCalib["data"]['attachments']:
                  hash1.update(attachment['data'].encode('cp1252','ignore'))
              for mask in LocalCalib["Masks"]:
                  hash2.update(open(mask["MaskFile"]).read().encode('cp1252','ignore'))
                  #hash2.update(base64.b64decode(base64.b64encode(open(mask["MaskFile"], "rb").read())).decode('cp1252','ignore'))
          if hash1.hexdigest()!=hash2.hexdigest():
              self.emit(QtCore.SIGNAL("ServerQueueChanged(QString)"), json.dumps(ServerCalib))