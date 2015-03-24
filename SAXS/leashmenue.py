
from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
import os,json,collections
import schematools,converter
import Leash
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
        self.queuemenue= self.app.menuBar().addMenu('&Queue')
        self.queueRedoAllImmagesAction =self.queuemenue.addAction("&Redo All Images")
        self.queueAbortAction=self.queuemenue.addAction("A&bort Queue")
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
        self.connect(self.actionImportFit2d, 
                      QtCore.SIGNAL("triggered()"),
                      self.importFit2d)
        self.connect(self.actionImportOlder, 
                      QtCore.SIGNAL("triggered()"),
                      self.importOlderJson)
        self.connect(self.queueRedoAllImmagesAction, 
                      QtCore.SIGNAL("triggered()"),
                      self.queueRedoAllImmages)
        self.userconffilename=os.path.expanduser(os.path.join('~',".saxsleashrc"))
        maxrecentfiles=5
        self.recentfiles=collections.deque( json.load(open(self.userconffilename))['recentFiles'], maxrecentfiles)
        self.recentfileactions=[]
        for i in range(maxrecentfiles):
            self.recentfileactions.append(self.filemenue.addAction(""))
        self.updaterecenfileslist()
    def importFit2d(self):
        self.importFrom("Open Fit2d Output Text File",converter.txt2json)
    def importOlderJson(self):
        self.importFrom("Open JSON From Older Versions",converter.jsontojson)
            
    def importFrom(self,buttontext,converterfun):
        dialog=QtGui.QDialog()
        layout=QtGui.QVBoxLayout()
        dialog.setLayout(layout)
        textarea=QtGui.QTextBrowser()
        textarea.setMinimumSize(600, 300)
        layout.addWidget(textarea)
        openbutton=QtGui.QPushButton(buttontext)
        layout.addWidget(openbutton)
        buttonbox=QtGui.QDialogButtonBox()
        cancelbutton=buttonbox.addButton(buttonbox.Cancel)
        okbutton=buttonbox.addButton(buttonbox.Ok)
        okbutton.setText("Import Data")
        layout.addWidget(buttonbox)
        self.connect(okbutton, QtCore.SIGNAL("clicked()"),dialog.accept)
        self.connect(cancelbutton, QtCore.SIGNAL("clicked()"),dialog.reject)
      
        def pickImportFile():
            filedialog=QtGui.QFileDialog()
            filename=filedialog.getOpenFileName()
            textarea.setText(open(filename).read())
        
        self.connect(openbutton, QtCore.SIGNAL("clicked()"),pickImportFile)
      
        def importText():
            text=unicode( textarea.toPlainText())
            if not  self.app.calibeditor.model.filename:
                 filedialog=QtGui.QFileDialog()
                 self.app.calibeditor.model.filename= unicode(filedialog.getSaveFileName(  caption= "Create New File AS" ))
            
            self.app.calibeditor.model.ifNoneInitFromDefault()
            converterfun(text,self.app.calibeditor.model.calib)
            self.app.calibeditor.model.rebuildModel()
            self.app.calibeditor.reset()
        self.connect(dialog, QtCore.SIGNAL("accepted()"),importText)
        dialog.exec_()
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
    def queueRedoAllImmages(self):
        argu=["readdir"]
        result=Leash.initcommand(self.app.options,argu,self.app.netconf)
        #self.log("reread directory")
        msgBox=QtGui.QMessageBox(self)
        msgBox.setText( result);
        msgBox.exec_();