
from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
import os,json,collections
import schematools
class menueitems(QtGui.QWidget):
    def __init__(self,app):
        super(menueitems, self).__init__()
        self.app=app
        self.filemenue=self.app.menuBar().addMenu('&File')
        self.actionOpen=self.filemenue.addAction("&Open")
        self.actionNew=self.filemenue.addAction("&New")
        self.importmenue= self.app.menuBar().addMenu('&Import')
        self.actionImportFit2d=self.importmenue.addAction("&Import Fit2d")
        self.actionImportOlder=self.importmenue.addAction("&Import Older SAXS calibration Files")
        self.actionSave=self.filemenue.addAction("&Save")
        self.actionSaveAs=self.filemenue.addAction("Save &As")
        self.connect(self.actionOpen, 
                     QtCore.SIGNAL("triggered()"),
                     self.openfile)
        self.connect(self.actionSave, 
                     QtCore.SIGNAL("triggered()"),
                     self.app.calibeditor.model.save)
        self.connect(self.actionSaveAs, 
                      QtCore.SIGNAL("triggered()"),
                      self.app.calibeditor.model.saveAs)
        self.connect(self.actionNew, 
                      QtCore.SIGNAL("triggered()"),
                      self.newfile)
        self.userconffilename=os.path.expanduser(os.path.join('~',".saxsleashrc"))
        maxrecentfiles=5
        self.recentfiles=collections.deque( json.load(open(self.userconffilename))['recentFiles'], maxrecentfiles)
        self.recentfileactions=[]
        for i in range(maxrecentfiles):
            self.recentfileactions.append(self.filemenue.addAction(""))
        self.updaterecenfileslist()
    def openfile(self):
       dialog=QtGui.QFileDialog()
       filename= unicode(dialog.getOpenFileName( ))
       print filename
       self.app.calibeditor.model.loadfile(filename)
       self.app.calibeditor.reset()
       self.appendrecentfile(filename)
    def newfile(self):
        dialog=QtGui.QFileDialog()
        filename= unicode(dialog.getSaveFileName(  caption= "Create New File AS" ))
        default= schematools.schematodefault(self.app.calibeditor.model.calschema)
        json.dump(
                 default,  open(filename,"w")
                  )
        self.app.calibeditor.model.loadfile(filename)
        self.app.calibeditor.reset()
        self.appendrecentfile(filename)
    def openrecent(self):
       action=self.sender()
       filename=unicode(action.data().toString ())
       self.app.calibeditor.model.loadfile(filename)
       self.app.calibeditor.reset()
       self.appendrecentfile(filename)
    def updaterecenfileslist(self):
        for i, file in enumerate(self.recentfiles):
            text = "&%d %s" % (i + 1, os.path.basename(file))
           
            self.recentfileactions[i].setText(text)
            self.recentfileactions[i].setData(file)
            self.recentfileactions[i].setToolTip ( file )
            self.connect(self.recentfileactions[i], QtCore.SIGNAL("triggered()"),self.openrecent)
    def appendrecentfile(self,filename):
        if filename in  self.recentfiles:
            self.recentfiles.remove(filename)
        self.recentfiles.appendleft(filename)
        self.updaterecenfileslist()
        self.saverecentfiles()
    def saverecentfiles(self):
        user=json.load(open(self.userconffilename))
        user["recentFiles"]=list(self.recentfiles)
        json.dump(user, open(self.userconffilename,"w"))