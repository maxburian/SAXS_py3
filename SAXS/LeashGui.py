import sys,os
import json

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import base64
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from multiprocessing import Process
from jsonschema import validate,ValidationError
from scipy.misc.pilutil import toimage
from PIL.ImageQt import ImageQt
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from PyQt4 import uic
import LeashMW
import atrdict
import calibration
from schematools import schematodefault
from Leash import initcommand
from plotthread import plotthread
from reconnectqthread import reconnecthread 
from ImportDialogClass import Importdialog
from converter import txt2json
from recentfilemenue import recentfilemenue
def nparrayToQPixmap(arrayImage):
    pilImage = toimage(arrayImage)
    
    qtImage = ImageQt(pilImage.convert("RGBA"))
    qImage = QImage(qtImage)
    qPixmap = QPixmap(qImage)
    return qPixmap

class LeashUI(QMainWindow):
    def __init__(self,app,parent=None):
        super(LeashUI,self).__init__(parent)
        self.clipboard=app.clipboard()
        self.ui=uic.loadUi(os.path.dirname(__file__)+os.sep+"LeashMW.ui",self)
        self.mainWindow=super(LeashUI,self)
        self.mainWindow.setWindowTitle("SAXS Leash")
        self.appdir=os.path.dirname(__file__)+os.sep
        self.mainWindow.setWindowIcon(QIcon(self.appdir+"icons"+os.sep+"program.png"))
        self.ui.tabWidget.setCurrentIndex(0)
        self.data=atrdict.AttrDict({})
        self.data.cal=None
        self.data.queueon=False
        self.ui.resize(1000,800)
        self.plotthread=QThread(parent=self)
        self.serveronline=False
        self.connect(self.ui.actionLoad_Calibration, SIGNAL("triggered()"),self.newFile)
        self.connect(self.ui.actionNew_Calibration, SIGNAL("triggered()"),self.newfromscratch)
        self.connect(self.ui.actionSave_Calibration,SIGNAL('triggered()'),self.safecalibration)
        self.connect(self.ui.actionSave_Calibration_as,SIGNAL('triggered()'),self.safecalibrationas)
        self.connect(self.ui.actionImport,SIGNAL('triggered()'),self.importcalib)
        self.connect(self.ui.actionAbort_Queue ,SIGNAL('triggered()'),self.abortqueue)
        self.connect(self.ui.actionClose_Queue ,SIGNAL('triggered()'),self.closequeue)
        self.connect(self.ui.actionShow_Server_Configuration ,SIGNAL('triggered()'),self.showserver)
        
        self.connect(self.ui.actionOpen_Hep_in_Browser ,SIGNAL('triggered()'),self.help)
   
        self.data.calschema=json.load(open(os.path.dirname(__file__)+os.sep+'schema.json')) 
        self.ui.treeWidgetCal.clear()
        self.ui.treeWidgetCal.setColumnWidth (0, 200 )
        self.ui.toolButtonRescale.setText("Fit to Window")
        self.connect(self.ui.toolButtonRescale, SIGNAL("clicked()"), self.resizemask)
        self.connect(self.ui.pushButtonLoadMask, SIGNAL("clicked()"), self.pickmask)
        self.ui.lineEditUserDir.setText(".")
        self.connect(self.ui.pushButtonnew, SIGNAL('clicked()'),self.commandnew)
        self.figure = plt.figure()
        self.figurehist=plt.figure()
        self.plotcanvas= FigureCanvas(self.figure)
        self.canvashist= FigureCanvas(self.figurehist)
        self.ui.verticalLayout_3.addWidget(self.plotcanvas)
        self.ylogchkbox=QCheckBox("Y Log Scale")
        self.ylogchkbox.setCheckState(2)
        self.ui.verticalLayout_3.addWidget(self.ylogchkbox)
     
        self.ui.verticalLayout_5.addWidget( self.canvashist)
        self.plotworker = plotthread(self)
        self.connect(self.ylogchkbox, SIGNAL("stateChanged(int)"),self.plotworker.setyscale)
        self.data.queueon=True
        self.recentfilemenue=recentfilemenue(self,self.ui.menuSAXS_Leash )
        self.connect(self.recentfilemenue, SIGNAL('openFile(QString)'),self.newFile)
        self.connect(self.plotworker, SIGNAL('update(QString)'),self.statupdate)
        self.errmsg=QErrorMessage(self)
        self.errmsg.setWindowTitle("Error")
        self.filename=""
        self.logbox= self.ui.textBrowserLogs
        self.log("hello")
      
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        QShortcut(QKeySequence("Ctrl+O"), self, self.newFile)
        QShortcut(QKeySequence("Ctrl+S"),self,self.safecalibration)
        QShortcut(QKeySequence("Ctrl+I"),self,self.importcalib)
        self.connect(self.ui,SIGNAL("reconnect()"),self.reconnect)
        if len( sys.argv)>1:
            if os.path.isfile(sys.argv[1]):
                print sys.argv[1]
                self.filename=sys.argv[1]
                self.newFile(filename=self.filename)
                self.plotworker.start()
                return
        self.emit(SIGNAL('reconnect()'))
    def newfromscratch(self):
        self.data.cal=schematodefault(self.data.calschema)
        self.ui.treeWidgetCal.clear()
        self.buildcaltree(self.data.cal, self.data.calschema,self.ui.treeWidgetCal)
        self.loadmask()
        self.filename="New.saxsconf"
        self.mainWindow.setWindowTitle("SAXS Leash | "+os.path.basename(self.filename)+"*")
    def newFile(self,filename=None):
      
        if filename:
            self.filename=unicode(filename)
        else:
            filename=unicode( 
                    QFileDialog.getOpenFileName(self  ,
                        caption="Open SAXS Calibration File" , 
                        filter="SAXS Config (*.saxsconf);;All files (*.*)"
                        ))
            if filename=="":
                return
            else:
                self.filename=filename
        
        try:
           
            filefh=open(self.filename,"r")
            self.data.cal=json.load(filefh)
            filefh.close()
            validate(self.data.cal,self.data.calschema)
        except ValueError as e: 
            dialog=QErrorMessage(self)
            dialog.showMessage(e.message)
            return
        except ValidationError as e:
            dialog=QErrorMessage(self)
            dialog.showMessage(e.message)
            return
        self.ui.treeWidgetCal.clear()
        self.recentfilemenue.append(self.filename)
        self.buildcaltree(self.data.cal,self.data.calschema,self.ui.treeWidgetCal)
        self.loadmask()
        self.mainWindow.setWindowTitle("SAXS Leash | "+os.path.basename(self.filename))
    def pickmask(self):
        if  self.data.cal is not None:
            self.data.cal['MaskFile']=unicode(
                    QFileDialog.getOpenFileName(self,
                        caption="Open SAXS Mask File" , 
                        filter="Fit2d Mask (*.msk);;All Image files (*.*)"
                        ))
            self.loadmask()
            self.ui.treeWidgetCal.clear()
            self.buildcaltree(self.data.cal, self.data.calschema,self.ui.treeWidgetCal)
        else:
            dialog=QErrorMessage(self)
            dialog.showMessage("Load a calibration file first!")
    def loadmask(self):
        try:
            self.data.mask=calibration.openmask(self.data.cal)
            image=nparrayToQPixmap(self.data.mask)
            self.data.qtmask=image
            maskscene=QGraphicsScene()
            maskscene.addPixmap(image)
        except IOError as e:
            dialog=QErrorMessage(self)
            dialog.showMessage(e.message)
            return
        self.ui.graphicsViewMask.setScene(maskscene)
        self.ui.graphicsViewMask.show()
        self.resizemask() 
    def resizemask(self):
        self.ui.graphicsViewMask.fitInView(QRectF(self.data.qtmask.rect()),Qt.KeepAspectRatio)
        self.ui.graphicsViewMask.show()
        
    def buildcaltree(self,cal,schema,tree):
        def walktree(cal,schema,tree):

            for key in schema['properties']:
                if key in cal:
                    entry=QTreeWidgetItem(tree)
                    entry.setText(0,key)
                    if  schema['properties'][key]["type"]=="object":
                        walktree(cal[key],schema['properties'][key], entry)
                        entry.setExpanded(True)
                        if not 'required' in  schema['properties'][key] or schema['properties'][key]['required']==False:
                            entry.setCheckState(1,Qt.Checked)
                    else:
                        entry.setText(1,str(cal[key]))
                        entry.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
                        
                        if "description" in  schema['properties'][key]:
                            entry.setToolTip(0, schema['properties'][key]["description"])
                        if "units" in schema['properties'][key]:
                            entry.setText(2,schema['properties'][key]['units'])
                   
                else:
                    entry=QTreeWidgetItem(tree)
                    entry.setText(0,key)
                    if not 'required' in  schema['properties'][key] or schema['properties'][key]['required']==False:
                        if schema['properties'][key]['type']=='object':
                            entry.setCheckState(1,Qt.Unchecked)
                        else:
                            entry.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.disconnect(self.ui.treeWidgetCal, SIGNAL("itemChanged(QTreeWidgetItem *,int)"),self.updatecalibration)
        walktree(cal,schema,tree)
        self.connect(self.ui.treeWidgetCal, SIGNAL("itemChanged(QTreeWidgetItem *,int)"),self.updatecalibration)
        
    def treetojson(self,tree,schema):
        jsoncal={}
        
        for position in range(tree.childCount()):
            child=tree.child(position)
            
            label= unicode(child.text(0))
            if  label in schema["properties"]:
                if schema["properties"][label]['type']=="string":
                    jsoncal[label]=unicode(child.text(1))
                if schema["properties"][label]['type']=="number": 
                    jsoncal[label]=float(unicode(child.text(1)))
                if schema["properties"][label]['type']=="integer":
                    jsoncal[label]=int(unicode(child.text(1)))
                if schema["properties"][label]['type']=="array":
                    jsoncal[label]=json.loads(unicode(child.text(1)))
                if schema["properties"][label]['type']=="object":
                    if 'required' not in schema["properties"][label] or schema["properties"][label]['required']==False:
                        if child.checkState(1):
                            if child.childCount()==0:
                                jsoncal[label]=schematodefault(schema["properties"][label])
                            else:
                                jsoncal[label]=self.treetojson(child,schema["properties"][label])
                        else:
                            pass
                    else:
                        jsoncal[label]=self.treetojson(child,schema["properties"][label])
                
        return jsoncal
    def updatecalibration(self):
        cal=self.treetojson(self.ui.treeWidgetCal.invisibleRootItem(), self.data.calschema)
        self.ui.treeWidgetCal.clear()
        try:
            validate(cal,self.data.calschema)
        except ValidationError as e:
            dialog=QErrorMessage(self)
            dialog.showMessage(e.message)
            self.buildcaltree(self.data.cal, self.data.calschema,self.ui.treeWidgetCal)
            return
        self.data.cal=cal
        self.buildcaltree(self.data.cal, self.data.calschema,self.ui.treeWidgetCal)
    def safecalibration(self):
        try:
            fh=open(self.filename,"w")
            json.dump(self.data.cal,fh)
            fh.close()
        except AttributeError:
            dialog=QErrorMessage(self)
            dialog.showMessage("Load file first")
            return
        QMessageBox(self).about(self,"saved",self.filename)
    def safecalibrationas(self):
        
        filename=unicode( QFileDialog.getSaveFileName(self, caption="Save SAXS Config File as" , 
                        filter="SAXS Config (*.saxsconf);;All files (*.*)" ))
        if filename=="":
            return
        else:
            self.filename=filename
        self.safecalibration()
        
    def commandnew(self):
        if self.data.cal:
            filename="tempcalfile"
            fh=open(filename,"w")
            json.dump(self.data.cal,fh)
            fh.close()
            conf=json.load(open(os.path.expanduser("~"+os.sep+".saxdognetwork")))
            argu=["new", filename,self.data.cal["MaskFile"], [
                             unicode(self.ui.lineEditUserDir.text()),
                             unicode(self.ui.lineEditExpDir.text()),
                             unicode(self.ui.lineEditSetupDir.text())]
                                                                        ]
            o=atrdict.AttrDict({"server":""})
            result=initcommand(o,argu,conf)
            print result
            self.ui.pushButtonnew.setText("Restart Queue with Changed Calibration")
            self.plotworker.start()
            self.log("New calibration loaded onto server.")
            os.remove(filename)
        else:
            dialog=QErrorMessage(self)
            dialog.showMessage("Load file first")
   
                    
    def statupdate(self,mesg):
   
        if unicode(mesg)=='data plotted':
            try:
                self.ui.lcdNumberFiles.display(self.data.stat['images processed'])
                self.ui.lcdNumberRate.display(self.data.stat['pics']/self.data.stat['time interval'])
                self.canvashist.draw()
                self.plotcanvas.draw()
            except:
                pass
        time.sleep(.2)
        if unicode(mesg)!='change yscale':
            self.plotworker.start()
        
    def cleanup(self):
        print "cleanup"
     
    def reconnect(self):
        self.data.result="{}"
        self.reconthread=reconnecthread(self)
        self.connect(self.reconthread,SIGNAL('error(QString)'),self.errmsg.showMessage)
        self.connect(self.reconthread,SIGNAL('connected(QString)'),self.buildcalfromserver)
        self.reconthread.start()
        self.timer=QTimer()
        self.timer.start(6000)
        self.connect(self.timer,SIGNAL('timeout()'),self.connectiontimeout)
    def connectiontimeout(self):
        self.timer.stop()
        if self.serveronline:
            self.log("Reconnected to server")
            pass
        else:
            self.errmsg.showMessage("Connection to server failed")
    def buildcalfromserver(self,result):
        self.serveronline=True
        try:
            #if there is no valid cal 
            validate(self.data.cal,self.data.calschema)
        except:
            # import new one
           
            try:
                resultjson=json.loads(unicode(result))
                cal=resultjson['data']['cal']
                 
            except KeyError as e:
                self.errmsg.showMessage("Server has no calibration.")
                return
            self.ui.treeWidgetCal.clear()
            try:
                validate(cal,self.data.calschema)
            except ValidationError as e:
                dialog=QErrorMessage(self)
                dialog.showMessage(e.message)
                self.buildcaltree(self.data.cal, self.data.calschema,self.ui.treeWidgetCal)
                return
            
            mskfilename=os.path.basename(cal['MaskFile'])
            print "maskfile:",mskfilename
            mskfile=open(mskfilename,'wb')
            cal['MaskFile']=mskfilename
            mskfile.write(base64.b64decode(resultjson['data']['mask']['data']))
            mskfile.close()
            self.data.cal=cal
            self.buildcaltree(self.data.cal, self.data.calschema,self.ui.treeWidgetCal)
            self.loadmask()
            self.directory=json.loads(unicode(result))['data']['directory']
            
            
           
            self.ui.lineEditUserDir.setText(self.directory[0])
            self.ui.lineEditExpDir.setText(self.directory[1])
            self.ui.lineEditSetupDir.setText(self.directory[2])
            self.log("Got calibration from server.")
            self.plotworker.start()
    def importcalib(self):
         
         self.importdialog=Importdialog(parent=self)
         self.importdialog.textEditbuffer.setText(self.clipboard.text())
         self.connect(self.importdialog.pushButtonLoadFile, SIGNAL("clicked()"),self.loadImortFile)
         self.connect(self.importdialog.pushButtonAbort,SIGNAL('clicked()'),self.importdialog.close)
         self.connect(self.importdialog.pushButtonOK,SIGNAL('clicked()'),self.importtext)
         self.importdialog.pushButtonLoadFile.setDefault(True)
         self.importdialog.show()
    def loadImortFile(self):
             file=unicode( QFileDialog.getOpenFileName(self,directory="../test"))
             self.importdialog.textEditbuffer.setText(open(file,"r").read())  
    def importtext(self):
        text=unicode(self.importdialog.textEditbuffer.toPlainText ())
        if not self.data.cal:
            self.data.cal=schematodefault(self.data.calschema)
        try:
            self.data.cal=txt2json(text,self.data.cal)
        except ValueError as e:
            self.errmsg.showMessage(e.message)
            return
        self.ui.treeWidgetCal.clear()
        self.buildcaltree(self.data.cal,self.data.calschema,self.ui.treeWidgetCal)
        self.importdialog.close()
    def abortqueue(self):
        argu=["abort"]
        o=atrdict.AttrDict({"server":""})
        conf=json.load(open(os.path.expanduser("~"+os.sep+".saxdognetwork")))
        result=initcommand(o,argu,conf)
        QMessageBox(self).about(self,"aborted",result)

    def closequeue(self):
        argu=["close"]
        o=atrdict.AttrDict({"server":""})
        conf=json.load(open(os.path.expanduser("~"+os.sep+".saxdognetwork")))
        result=initcommand(o,argu,conf) 
        QMessageBox(self).about(self,"closed",result)
    def help(self):
        import webbrowser
        webbrowser.open('http://christianmeisenbichler.github.io/SAXS/Server.html')
    def showserver(self):
        dialog=QDialog(self)
        dialog.setWindowTitle("Server Status")
        textfield=QTextBrowser()
        try:
            serverc=json.load(open(os.path.expanduser(os.path.join("~",".saxdognetwork"))))
        except IOError:
            self.errmsg.showMessage("No network configuration in '~/.saxdognetwork'. Use the 'saxsnetconf' command line tool to create one.")
            
        textfield.append(json.dumps(serverc,indent=4, separators=(',', ': ')))
        status=QLabel(self)
        if self.serveronline:
            status.setText("Server Connected")
        else:
            status.setText("Server Offline")
        layout=QVBoxLayout( )
        layout.addWidget(textfield)
        layout.addWidget(status)
        dialog.setLayout(layout)
        dialog.exec_()
    def log(self,text):
        
        self.logbox.append(str(datetime.datetime.now())+": "+text)
def LeashGUI():
    app=QApplication(sys.argv)
    form=LeashUI(app)
    form.show()
    app.exec_()
    form.cleanup()
if __name__ == "__main__":
    LeashGUI()
    