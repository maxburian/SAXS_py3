import os
import collections
import json
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
class recentfilemenue(QtCore.QObject):
    """
    populates and manages recent files list in File menue
    """
    def __init__(self,mw,fmenue):
        super(recentfilemenue,self).__init__()
        self.maxrecentfiles=5
        self.mw=mw
        self.fmenue=fmenue
        self.open=open
        self.recenfileQactions=[]
        for i in  range(  self.maxrecentfiles): 
            self.recenfileQactions.append( QtGui.QAction(self.mw, 
                            visible=False,
                            triggered=self.openRecentFile))
        self.userconffilename=os.path.expanduser(os.path.join('~',".saxsleashrc"))
        self.openuserconf()
        self.files=collections.deque(self.userconf["recentFiles"], self.maxrecentfiles)
        self.addtomenue() 
        self.updaterecentfilelist()
        
    def openuserconf(self):
        try:
            self.userconf=json.load(open(self.userconffilename))
        except:
          self.userconf={"recentFiles":[]}
          json.dump(self.userconf,open(self.userconffilename,"w"))   
    def updaterecentfilelist(self):
        for i,file in enumerate(self.files):   
            text = "&%d %s" % (i + 1, os.path.basename(file))
            self.recenfileQactions[i].setText(text)
            self.recenfileQactions[i].setData(file)
            self.recenfileQactions[i].setVisible(True)
    def addtomenue(self):
        
        for i in range( self.maxrecentfiles):
            self.fmenue.addAction(  self.recenfileQactions[i])
    def append(self,filename):
        if filename in  self.files:
            self.files.remove(filename)
        self.files.appendleft(filename)
        self.updaterecentfilelist()
        self.save()
    def save(self):
        self.openuserconf()
        self.userconf["recentFiles"]=list(self.files)
        json.dump(self.userconf,open(self.userconffilename,"w"))
        
    def openRecentFile(self): 
        action = self.sender()
     
        if action:
            self.emit(QtCore.SIGNAL('openFile(QString)'), action.data().toString () )