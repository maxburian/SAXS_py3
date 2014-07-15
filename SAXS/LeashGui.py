import sys,os
import json

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
 

import matplotlib.pyplot as plt
from multiprocessing import Process
from jsonschema import validate,ValidationError
from scipy.misc.pilutil import toimage
from PIL.ImageQt import ImageQt
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from PyQt4 import uic
import LeashMW
import SAXS
from schematools import schematodefault
from Leash import initcommand
from plotthread import plotthread
from reconnectqthread import reconnecthread 
def nparrayToQPixmap(arrayImage):
    pilImage = toimage(arrayImage)
    
    qtImage = ImageQt(pilImage.convert("RGBA"))
    qImage = QImage(qtImage)
    qPixmap = QPixmap(qImage)
    return qPixmap

class LeashUI(QMainWindow):
    def __init__(self,parent=None):
        super(LeashUI,self).__init__(parent)
        self.ui=uic.loadUi(os.path.dirname(__file__)+os.sep+"LeashMW.ui",self)
        self.data=SAXS.AttrDict({})
        self.data.cal=None
        self.data.queueon=False
        self.ui.resize(1000,800)
        self.plotthread=QThread(parent=self)
        
        self.connect(self.ui.actionLoad_Calibration, SIGNAL("triggered()"),self.newFile)
        self.connect(self.ui.actionSave_Calibration,SIGNAL('triggered()'),self.safecalibration)
        self.connect(self.ui.actionSave_Calibration_as,SIGNAL('triggered()'),self.safecalibrationas)
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
        self.ui.verticalLayout_5.addWidget( self.canvashist)
        self.plotworker = plotthread(self)
        self.data.queueon=True
        self.connect(self.plotworker, SIGNAL('update(QString)'),self.plotcanvas.draw)   
        self.connect(self.plotworker, SIGNAL('update(QString)'),self.statupdate)
        self.errmsg=QErrorMessage(self)
       
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        QShortcut(QKeySequence("Ctrl+O"), self, self.newFile)
        QShortcut(QKeySequence("Ctrl+S"),self,self.safecalibration)
        self.connect(self.ui,SIGNAL("reconnect()"),self.reconnect)
        self.emit(SIGNAL('reconnect()'))
    def newFile(self):
        filename=unicode( QFileDialog.getOpenFileName(self,directory="../test"))
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
        
        self.buildcaltree(self.data.cal,self.data.calschema,self.ui.treeWidgetCal)
        self.loadmask()
    def pickmask(self):
        if  self.data.cal is not None:
            self.data.cal['MaskFile']=unicode(QFileDialog.getOpenFileName(self,directory="../doc"))
            self.loadmask()
            self.ui.treeWidgetCal.clear()
            self.buildcaltree(self.data.cal, self.data.calschema,self.ui.treeWidgetCal)
        else:
            dialog=QErrorMessage(self)
            dialog.showMessage("Load a calibration file first!")
    def loadmask(self):
        try:
            self.data.mask=SAXS.openmask(self.data.cal)
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
        
        filename=unicode( QFileDialog.getOpenFileName(self,directory="../test"))
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
            argu=["new", filename,self.data.cal["MaskFile"],os.sep.join([
                             unicode(self.ui.lineEditUserDir.text()),
                             unicode(self.ui.lineEditExpDir.text()),
                             unicode(self.ui.lineEditSetupDir.text())]
                                                                        )]
            o=SAXS.AttrDict({"server":""})
            result=initcommand(o,argu,conf)
            print result
            self.ui.pushButtonnew.setText("Restart Queue with Changed Calibration")
            self.plotworker.start()
            os.remove(filename)
        else:
            dialog=QErrorMessage(self)
            dialog.showMessage("Load file first")
   
                    
    def statupdate(self):
        
        self.ui.lcdNumberFiles.display(self.data.stat['images processed'])
        self.ui.lcdNumberRate.display(self.data.stat['pics']/self.data.stat['time interval'])
        self.canvashist.draw()
    def cleanup(self):
        print "cleanup"
        self.plotthreadgo=False
    def reconnect(self):
        self.data.result="{}"
        self.reconthread=reconnecthread(self)
        self.connect(self.reconthread,SIGNAL('error(QString)'),self.errmsg.showMessage)
        self.connect(self.reconthread,SIGNAL('connected(QString)'),self.buildcalfromserver)
        self.reconthread.start()
    def buildcalfromserver(self,result):
        print  unicode(result)
        try:
            cal=json.loads(unicode(result))['data']['cal']
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
        self.data.cal=cal
        self.buildcaltree(self.data.cal, self.data.calschema,self.ui.treeWidgetCal)
        self.loadmask()
        self.plotworker.start()
        
if __name__ == "__main__":
    app=QApplication(sys.argv)
    form=LeashUI()
    form.show()
    app.exec_()
    form.cleanup()
        