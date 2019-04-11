
from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
from PyQt4.Qt import QMessageBox
import os, json, collections
import ctypes
from . import schematools, converter
from . import Leash
class menueitems(QtGui.QWidget):
    def __init__(self, app):
        super(menueitems, self).__init__()
        self.app=app
        self.errormessage=QtGui.QErrorMessage()
        self.filemenue=self.app.menuBar().addMenu('&File')
        self.actionOpen=self.filemenue.addAction("&Open")
        self.actionNew=self.filemenue.addAction("&New")
        self.importmenue= self.app.menuBar().addMenu('&Import')
        self.actionImportFit2d=self.importmenue.addAction("&Import Fit2d")
        self.actionImportOlder=self.importmenue.addAction("&Import Older SAXS calibration Files")
        self.actionConvertFromNika=self.importmenue.addAction("&Convert from NIKA values")
        self.actionSave=self.filemenue.addAction("&Save")
        self.actionSaveAs=self.filemenue.addAction("Save &As")
        self.filemenue.addSeparator()
        self.queuemenue= self.app.menuBar().addMenu('&Queue')
        self.queueRedoAllImmagesAction =self.queuemenue.addAction("&Redo All Images")
        self.queueAbortAction=self.queuemenue.addAction("A&bort Queue")
        self.helpmenue=self.app.menuBar().addMenu('&Help')
        self.openhelpbrowser=self.helpmenue.addAction("&Online Help")
        self.connect(self.openhelpbrowser, 
                     QtCore.SIGNAL("triggered()"),
                     self.help)
        self.connect(self.queueAbortAction, 
                     QtCore.SIGNAL("triggered()"),
                     self.abortqueue)
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
        self.connect(self.actionConvertFromNika, 
                      QtCore.SIGNAL("triggered()"),
                      self.convertFromNika)
        self.connect(self.queueRedoAllImmagesAction, 
                      QtCore.SIGNAL("triggered()"),
                      self.queueRedoAllImmages)
        self.userconffilename=os.path.expanduser(os.path.join('~', ".saxsleashrc"))
        if not os.path.isfile(self.userconffilename):
            content={"recentFiles": ["","","","",""]}
            json.dump(content, open(self.userconffilename, "w"))
        maxrecentfiles=5
        self.recentfiles=collections.deque(json.load(open(self.userconffilename))['recentFiles'], maxrecentfiles)
        self.recentfileactions=[]
        for i in range(maxrecentfiles):
            self.recentfileactions.append(self.filemenue.addAction(""))
            self.connect(self.recentfileactions[i], QtCore.SIGNAL("triggered()"), self.openrecent)
        self.updaterecenfileslist()
    def importFit2d(self):
        self.importFrom("Open Fit2d Output Text File", converter.txt2json)
    def importOlderJson(self):
        self.importFrom("Open JSON From Older Versions", converter.jsontojson)
        
    def importFrom(self, buttontext, converterfun):
        dialog=QtGui.QDialog()
        dialog.setWindowTitle("Import calibbration...")
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
        self.connect(okbutton, QtCore.SIGNAL("clicked()"), dialog.accept)
        self.connect(cancelbutton, QtCore.SIGNAL("clicked()"), dialog.reject)
      
        def pickImportFile():
            filedialog=QtGui.QFileDialog()
            filename=filedialog.getOpenFileName()
            textarea.setText(open(filename).read())
        
        self.connect(openbutton, QtCore.SIGNAL("clicked()"), pickImportFile)
      
        def importText():
            text=str(textarea.toPlainText())
            if not self.app.calibeditor.model.filename:
                 filedialog=QtGui.QFileDialog()
                 self.app.calibeditor.model.filename= str(filedialog.getSaveFileName(  caption= "Create New File AS" ))
            
            self.app.calibeditor.model.ifNoneInitFromDefault()
            converterfun(text, self.app.calibeditor.model.calib)
            self.app.calibeditor.model.rebuildModel()
            self.app.calibeditor.reset()
        self.connect(dialog, QtCore.SIGNAL("accepted()"), importText)
        dialog.exec_()
        
    def convertFromNika(self):
        dialog=QtGui.QDialog()
        layout=QtGui.QFormLayout()
        dialog.setWindowTitle("Convert calibbration from NIKA 2D...")
        
        radiobox=QtGui.QHBoxLayout()
        r1M = QtGui.QRadioButton("Pilatus 1M")
        radiobox.addWidget(r1M)
        r100K = QtGui.QRadioButton("Pilatus 100K")
        radiobox.addWidget(r100K)
        r100K.setChecked(True)
        ldet=QtGui.QLabel('Select detector:')
        layout.addRow(ldet,radiobox)
        
        eX = QtGui.QLineEdit()
        eX.setValidator(QtGui.QDoubleValidator(-99999,99999,2))
        eX.setMaxLength(7)
        eX.setAlignment(QtCore.Qt.AlignRight)
        lX=QtGui.QLabel('X Beamcenter: [pixel]')
        layout.addRow(lX,eX)
        
        eY = QtGui.QLineEdit()
        eY.setValidator(QtGui.QDoubleValidator(-99999,99999,2))
        eY.setMaxLength(7)
        eY.setAlignment(QtCore.Qt.AlignRight)
        lY = QtGui.QLabel('Y Beamcenter: [pixel]')
        layout.addRow(lY,eY)
        
        eSD = QtGui.QLineEdit()
        eSD.setValidator(QtGui.QDoubleValidator(-99999,99999,2))
        eSD.setMaxLength(7)
        eSD.setAlignment(QtCore.Qt.AlignRight)
        lSD = QtGui.QLabel('Sanple-Detector distance: [mm]')
        layout.addRow(lSD,eSD)
        
        eWL = QtGui.QLineEdit()
        eWL.setValidator(QtGui.QDoubleValidator(-99999,99999,2))
        eWL.setMaxLength(7)
        eWL.setAlignment(QtCore.Qt.AlignRight)
        eWL.setText("1.54")
        lWL = QtGui.QLabel('Wavelength: [Angs]')
        layout.addRow(lWL,eWL)
        
        erX = QtGui.QLineEdit()
        erX.setValidator(QtGui.QDoubleValidator(-99999,99999,2))
        erX.setMaxLength(7)
        erX.setAlignment(QtCore.Qt.AlignRight)
        erX.setText("0")
        lrX = QtGui.QLabel('Horizontal Rotation: [deg]')
        layout.addRow(lrX,erX)
        
        erY = QtGui.QLineEdit()
        erY.setValidator(QtGui.QDoubleValidator(-99999,99999,2))
        erY.setMaxLength(7)
        erY.setAlignment(QtCore.Qt.AlignRight)
        erY.setText("0")
        lrY = QtGui.QLabel('Vert Rotation: [deg]')
        layout.addRow(lrY,erY)
        
        buttonbox=QtGui.QDialogButtonBox()
        cancelbutton=buttonbox.addButton(buttonbox.Cancel)
        okbutton=buttonbox.addButton(buttonbox.Ok)
        okbutton.setEnabled(False)
        layout.addRow(buttonbox)  
        dialog.setLayout(layout)
        self.connect(okbutton, QtCore.SIGNAL("clicked()"), dialog.accept)
        self.connect(cancelbutton, QtCore.SIGNAL("clicked()"), dialog.reject)
        
        def checkValues():
            valuesok = False
            try:
                eXd=float(eX.text())
                eYd=float(eY.text())
                erXd=float(erX.text())
                erYd=float(erY.text())
                eSDd=float(eSD.text())
                eSDd=float(eWL.text())
                valuesok = True
            except:
                valuesok = False
                
            if valuesok == True:
                okbutton.setEnabled(True)
            else:
                okbutton.setEnabled(False)
                
            
        def importValues():
            try:
                eXd=float(eX.text())
                eYd=float(eY.text())
                erXd=float(erX.text())
                erYd=float(erY.text())
                eSDd=float(eSD.text())
                eWLd=float(eWL.text())
                '''det defines Detector type. det=1: 1M, det=2: 100K, etc..'''
                if r1M.isChecked() == True:
                    det = 1
                if r100K.isChecked() == True:
                    det = 2
            except:
                ctypes.windll.user32.MessageBoxA(0, "There seems to be a problem with your input. Check Again!".encode('ascii'), "Input:".encode('ascii'), 0x0|0x30)      
                return
            if not self.app.calibeditor.model.filename:
                 filedialog=QtGui.QFileDialog()
                 self.app.calibeditor.model.filename= str(filedialog.getSaveFileName(caption= "Create New File AS" ))
        
            
            self.app.calibeditor.model.ifNoneInitFromDefault()
            converter.nika2json(det, eXd,eYd,erXd,erYd, eSDd, eWLd, self.app.calibeditor.model.calib) 
            self.app.calibeditor.model.rebuildModel()
            self.app.calibeditor.reset()
            
        self.connect(eX, QtCore.SIGNAL("textChanged(QString)"), checkValues)
        self.connect(eY, QtCore.SIGNAL("textChanged(QString)"), checkValues)
        self.connect(erX, QtCore.SIGNAL("textChanged(QString)"), checkValues)
        self.connect(erY, QtCore.SIGNAL("textChanged(QString)"), checkValues)
        self.connect(eSD, QtCore.SIGNAL("textChanged(QString)"), checkValues)
        self.connect(eWL, QtCore.SIGNAL("textChanged(QString)"), checkValues)
        
        self.connect(dialog, QtCore.SIGNAL("accepted()"), importValues)       
        dialog.exec_()
                
    def openfile(self):
       dialog=QtGui.QFileDialog()
       filename= str(dialog.getOpenFileName( ))
       print(filename)
       self.app.calibeditor.model.loadfile(filename)
       self.app.calibeditor.reset()
       self.appendrecentfile(filename)
    def newfile(self):
        dialog=QtGui.QFileDialog()
        filename= str(dialog.getSaveFileName(  caption= "Create New File AS" ))
        default= schematools.schematodefault(self.app.calibeditor.model.schema)
        json.dump(
                 default,  open(filename, "w")
                  )
        self.app.calibeditor.model.loadfile(filename)
        self.app.calibeditor.reset()
        self.appendrecentfile(filename)
        print("self.app.calibeditor.model.filename", self.app.calibeditor.model.filename)
    def openrecent(self):
       action=self.sender()
       filename=str(action.data())
       #print(filename+"*")
       self.app.calibeditor.model.loadfile(filename)
       self.app.calibeditor.reset()
       self.appendrecentfile(filename)
    def updaterecenfileslist(self):
        for i, file in enumerate(self.recentfiles):
            text = "&%d %s" % (i + 1, os.path.basename(file))
           
            self.recentfileactions[i].setText(text)
            self.recentfileactions[i].setData(file)
            self.recentfileactions[i].setToolTip ( file )
            
    def appendrecentfile(self, filename):
        if filename in  self.recentfiles:
            self.recentfiles.remove(filename)
        self.recentfiles.appendleft(filename)
        self.updaterecenfileslist()
        self.saverecentfiles()
        
    def saverecentfiles(self):
        user=json.load(open(self.userconffilename))
        user["recentFiles"]=list(self.recentfiles)
        json.dump(user, open(self.userconffilename, "w"))
    def queueRedoAllImmages(self):
        argu=["readdir"]
        result=json.loads(Leash.initcommand(self.app.options, argu, self.app.netconf))
        print(result)
        try:
            access = result["data"]["Error"]
            self.errormessage.setWindowTitle("Server Error")
            self.errormessage.setMinimumSize(400, 300)
            self.errormessage.showMessage(result["data"]["Error"])
        except:
            titlestr=result["result"]
            #res=QMessageBox.information(self, self.tr("Restart..."),self.tr(titlestr), QMessageBox.Ok,QMessageBox.Ok)
            msgBox=QtGui.QMessageBox(self)
            msgBox.setText(str(titlestr));
            msgBox.exec_();

    def abortqueue(self):
        argu=["abort"]
        result=json.loads(Leash.initcommand(self.app.options, argu, self.app.netconf))
        self.emit(QtCore.SIGNAL('queueaborted()'))
        msgBox=QtGui.QMessageBox(self)
        msgBox.setText( result["result"]);
        msgBox.exec_();
    def help(self):
        import webbrowser
        webbrowser.open('http://ac-software.tugraz.at/SAXS')
        
        
        
        