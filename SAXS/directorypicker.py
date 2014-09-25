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
        print dirlist
        for i, box in enumerate(self.comboBox):
            box.clear()
            if i<len(dirlist):
                dirname=dirlist[i]
                dir =os.sep.join(dirlist[:i])
                print "dir: "+ dirname +str(i)+"path: "+dir
                if dirname!="":
                    self.fillbox(self.comboBox[i], dir,selected=dirname)
                elif dirlist[i-1]!="":
                    self.fillbox(self.comboBox[i], dir)
        self.dirlist=dirlist   
        print "set dirlist"
        print self.dirlist  
              
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
            if dir=="-": dir=""
            dirlist.append(dir)
            
        return dirlist
    def update(self):
        dirlist=self.getdirlist()
        print dirlist
        changed=False
        for i, dir in enumerate(dirlist):
            if i<len(self.comboBox)-1:
                if changed:
                    self.comboBox[i+1].blockSignals(True)
                    self.comboBox[i+1].clear()
                    self.comboBox[i+1].blockSignals(False)
                elif dir!=self.dirlist[i] and not dir=="":
                    listpath="."+os.sep+os.sep.join(dirlist[:i+1] )
                    print "lp"+ listpath
                    self.fillbox(self.comboBox[i+1], listpath,dirlist[i+1])
                    changed=True
                elif dir=="":
                    self.comboBox[i+1].blockSignals(True)
                    self.comboBox[i+1].clear()
                    self.comboBox[i+1].blockSignals(False)
                    changed=True
               
        self.dirlist=dirlist