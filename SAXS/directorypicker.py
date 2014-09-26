from Leash import initcommand
from PyQt4.QtCore import *
from PyQt4.QtGui import  *
import json,os
import atrdict
class directorypicker(QThread ):
    """
    This class handles the directory picker
    """
    def __init__(self,app,cboxlist=None):
        QThread.__init__(self)
        if not cboxlist:
            self.comboBox=[]
            self.comboBox.append(app.ui.comboBoxUser)
            self.comboBox.append( app.ui.comboBoxExperiment)
            self.comboBox.append(app.ui.comboBoxSetup)
        else:
            self.comboBox=cboxlist
        self.MW=app.mainWindow
        self.netconf=json.load(open(os.path.expanduser("~"+os.sep+".saxsdognetwork")))
        for box in self.comboBox:
            self.connect(box, SIGNAL("currentIndexChanged( int)"),self.update)
        self.dirlist=[]
    def setdir(self,dirlist): 
        
       
        if dirlist[0]=="":
            dirlist[0] ="."
        for i, box in enumerate(self.comboBox):
            box.blockSignals(True)
            box.clear()
            if i<len(dirlist) and dirlist[i]!="":
                dirname=dirlist[i]
                dir =os.sep.join(dirlist[:i])
                if dirname!="" :
                    self.fillbox(self.comboBox[i], dir,selected=dirname)
                elif dirlist[i-1]!=""  :
                    self.fillbox(self.comboBox[i], dir)
            box.blockSignals(False)
        self.dirlist=dirlist   
              
    def fillbox(self,box,path,selected="-"):
        currentdirname=os.path.dirname(path)
        
        argu=["listdir",os.sep.join(path.split(os.sep))]
        o=atrdict.AttrDict({"server":""})
        result=json.loads(  initcommand(o,argu,self.netconf))
        i=1
        box.blockSignals(True)
        box.clear()
        box.addItem("-")
        box.setCurrentIndex(0)
        if 'dircontent' in result['data']:
            for  dir in  result['data']['dircontent']:
                if dir['isdir']:
                    box.addItem(dir['path'])
                    if dir['path']==selected:
                        box.setCurrentIndex(i)
                       
                    i=i+1
        box.blockSignals(False)
    def getdirlist(self):
        dirlist=[]
        for i, box in enumerate(self.comboBox):
            dir=unicode(box.currentText())
            if dir=="-": 
                dir=" "
                return dirlist
            if dir!=" ":
                dirlist.append(dir)
            
        return dirlist
    def update(self):
        dirlist=self.getdirlist()
        changed=False
        
        for i, box in enumerate(self.comboBox):
            box.blockSignals(True)
            if changed:
                if i < len (dirlist):
                    dirlist[i]=" "
                box.clear()
            elif self.prevdirhaschanged(dirlist,i):
                 changed=True
                 if self.previousdir(dirlist,i)==" ":
                     box.clear()
                     if i < len (dirlist):
                         dirlist[i]=" "
                 else:
                     self.fillbox(box, os.sep.join(dirlist[0:i]))
                     if i < len (dirlist):
                         dirlist[i]=" "
                 
            box.blockSignals(False)
        self.dirlist=dirlist
    def prevdirhaschanged(self,dirlist,i):
        if i==0:
            return False
        if len(dirlist)>=i:
            newd=dirlist[i-1]
        else:
            newd=" "
        if len(self.dirlist)>=i:
            oldd=self.dirlist[i-1]
        else:
            oldd=" "
        if newd!=oldd:
            return True
        else:
            return False
    def previousdir(self,dirlist,i):
        if i==0:
            prevdir="."
        if len(dirlist)>=i:
            prevdir=dirlist[i-1]
        else:
            prevdir=" "
        return prevdir
        