from PyQt4 import  QtGui
from PyQt4 import  QtCore
import json, os, collections
from . import jsonschematreemodel
from . import calibeditdelegate
from . import schematools
from jsonschema import validate, ValidationError
from . import Leash
import time
from datetime import datetime
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt
import prettyplotlib as ppl
class consolidatepanel(QtGui.QWidget):
    def __init__(self, app):
        super(consolidatepanel, self).__init__( )
        self.app=app
        
        self.localmergetstatusthread = mergestatusthread(self)
        self.timeformat = "%Y.%m.%d - %H:%M:%S"
        self.connect(self.localmergetstatusthread, QtCore.SIGNAL("sig_writeToStatus(QString)"), self.writeToStatus)
        
        self.hlayout=QtGui.QHBoxLayout()
        self.setLayout(self.hlayout)
        
        self.vlayout=QtGui.QVBoxLayout()
        self.hlayout.addLayout(self.vlayout)
        
        self.treeview=QtGui.QTreeView()
        self.vlayout.addWidget(self.treeview)
        
        self.statuslabel =QtGui.QLabel()
        self.vlayout.addWidget(self.statuslabel)
        self.statuslabel.setText("Datamerger status:")
        
        self.statusfield = QtGui.QTextEdit()
        self.vlayout.addWidget(self.statusfield)
        self.statusfield.setMaximumHeight(150)
        self.statusfield.setMinimumHeight(150)
        self.statusfield.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.statusfield.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        
        self.model=jsonschematreemodel.jsonschematreemodel( app,
                        schema=json.load(open(os.path.dirname(__file__)
                        +os.sep+'DataConsolidationConf.json'),
                        object_pairs_hook=collections.OrderedDict) 
                                                           )
        self.treeview.setModel(self.model)
        self.treeview.setMinimumWidth(400)
        self.treeview.setMinimumHeight(400)
        self.treeview.setAlternatingRowColors(True)
        self.treeview.setItemDelegateForColumn(1, calibeditdelegate.calibEditDelegate( app ))
        self.reset()
        default= schematools.schematodefault(self.model.schema)
        
        
        self.filename=os.path.expanduser("~"
                                               +os.sep
                                               +self.app.netconf["Name"]
                                               +"consolconf.json"
                                               )
        if not os.path.isfile(self.filename):
            import shutil
            shutil.copy(os.path.dirname(__file__)   +os.sep+'consolconftemplate.json', self.filename)
        
        try:
            self.calib=json.load(open(self.filename), object_pairs_hook=collections.OrderedDict)
            validate(self.calib, self.model.schema)
        except Exception as e:
            print(e)
            import shutil
            shutil.copy(os.path.dirname(__file__)   +os.sep+'consolconftemplate.json', self.filename)
         
        self.model.loadfile(self.filename)
        self.reset()
        self.connect(self.model, QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'), self.model.save)
        self.submitbutton=QtGui.QPushButton("Collect All Data")
        self.submitbutton.setEnabled(False)
        self.submitbutton.setMinimumWidth(150)
        self.submitbutton.setMaximumWidth(150)
        
        self.submitlabel=QtGui.QLabel("Waiting for calibration...")
        
        self.submitlayout=QtGui.QVBoxLayout()
        
        self.hlayout.addLayout(self.submitlayout)
        self.submitlayout.addWidget(self.submitlabel)
        self.submitlayout.addWidget(self.submitbutton)
        self.submitlayout.addStretch()
        
        self.connect(self.submitbutton, QtCore.SIGNAL("clicked()"), self.startmerge)
        self.connect(self.app.plotthread, QtCore.SIGNAL("mergeresultdata(QString)"), self.showmergeresults)
        
        self.writeToStatus("\nDatamerger waiting for input... Make sure you load a calibration first!")

    def reset(self):
        self.model.invisibleRootItem().setColumnCount(3)
        self.treeview.setColumnWidth(0, 320)
        self.treeview.setColumnWidth(1, 320)
        self.treeview.expandAll()
        
    def startmerge(self):
        mergeok = self.checkinput()
        if mergeok == "OK":
            argu=["mergedata", self.filename]
            result=json.loads(Leash.initcommand(self.app.options, argu, self.app.netconf))
            print(result)
            if result['result']=="Error" or result['result']=="ServerError":
                errormessage=QtGui.QErrorMessage(parent=self.app)
                errormessage.setWindowTitle("Server Error")
                errormessage.setMinimumSize(400, 300)
                errormessage.showMessage(result['data']["Error"])
            else:
                self.localmergetstatusthread.start()
                self.statusfield.clear()
                self.writeToStatus("\n\n******************************************")
                tempstr = str(datetime.now().strftime(self.timeformat)) + ": Datamerge has started!" 
                self.writeToStatus(tempstr)
                self.writeToStatus("******************************************")
                
                self.submitlabel.setText("Merging data!")
                self.submitbutton.setEnabled(False)
                self.app.submitbutton.setEnabled(False)
        else:
            errormessage=QtGui.QErrorMessage(parent=self.app)
            errormessage.setWindowTitle("Configuration Error")
            errormessage.setMinimumSize(400, 300)
            errormessage.showMessage(mergeok)
            
    def showmergeresults(self, qstringdata):
        try :
            result=json.loads(str(qstringdata))
            import pandas as pd
            dialog=QtGui.QDialog()
            dialog.setWindowTitle("Merge Sucessfull")
            vlayout=QtGui.QVBoxLayout()
            dialog.setLayout(vlayout)
            figure=plt.figure( )
            ax=figure.add_subplot(111)
            canvas= FigureCanvas(figure)
            navbar=NavigationToolbar(canvas, dialog)
            vlayout.addWidget(canvas)
            vlayout.addWidget(navbar)
            img=pd.io.json.read_json(json.dumps(result["data"]["syncplot"]['Images'])).transpose()
            peak= pd.io.json.read_json(json.dumps(result["data"]["syncplot"]['Shutter'])).transpose()
            peak=peak[peak>0]
            img.plot(style="ro", ax=ax)  
            peak.plot(style="x", ax=ax)
            canvas.draw() 
            if "CalculatedTimeshift" in result["data"]["syncplot"]:
                timelabel=QtGui.QLabel("Calculated time Shift: "
                                       +result["data"]["syncplot"]['CalculatedTimeshift'])
                vlayout.addWidget(timelabel)
            dialog.exec_()
        except Exception as e:
            print(e)
            self.writeToStatus("Something went wrong plotting: merge was still succesfull!")
                               
        self.localmergetstatusthread.quit()
        self.writeToStatus("******************************************")
        tempstr = str(datetime.now().strftime(self.timeformat)) + ": Datamerge has finihsed!" 
        self.writeToStatus(tempstr)
        self.writeToStatus("******************************************")
        
        self.submitlabel.setText("Ready...")
        self.submitbutton.setEnabled(True)
        self.app.submitbutton.setEnabled(True)
    
    def checkinput(self):
        mergeok = "OK"
        cal=json.load(open(self.filename, "r"))
        for table in cal["LogDataTables"]:
            if table["FirstImageCorrelation"]==True and table["Name"]!="Peak":
                mergeok = "Image correlation only makes sense with Peak-Integ file."
                break
            if table["ZeroImageCorrelation"]==True and table["Name"]!="Peak":
                mergeok = "Zero correlation only makes sense with Peak-Integ file."
                break
            if table["FirstImageCorrelation"]==True and table["ZeroImageCorrelation"]==True :
                mergeok = "Zero.tif and First-Image correlation is not possible. Choose one of them."
                break
        return mergeok
    
    def writeToStatus(self, text):
        if text[0:1]=="\n":
            text = text[1:]
        self.statusfield.append(text)
        if "---ERROR---" in text:
            self.submitbutton.setEnabled(True)
            self.app.submitbutton.setEnabled(True) 
        
        
class mergestatusthread(QtCore.QThread):
    def __init__(self, app):
        super(mergestatusthread, self).__init__()
        self.app = app
        self.returnstring = ""
        
    def run(self):
        while True:
            argu = ["getmergestat"]
            returndict = json.loads(Leash.initcommand(self.app.app.options, argu, self.app.app.netconf))
            self.returnstring = returndict['data']["mergeinfo"]
            if self.returnstring!="":
                self.emit(QtCore.SIGNAL('sig_writeToStatus(QString)'), self.returnstring)
                #self.app.writeToStatus(self.returnstring)
            time.sleep(1)
                