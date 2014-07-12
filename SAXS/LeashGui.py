import sys,os
import json
from jsonschema import validate,ValidationError
from scipy.misc.pilutil import toimage
from PIL.ImageQt import ImageQt
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from PyQt4 import uic
import LeashMW
import SAXS
def nparrayToQPixmap(arrayImage):
    pilImage = toimage(arrayImage)
    
    qtImage = ImageQt(pilImage.convert("RGBA"))
    qImage = QImage(qtImage)
    qPixmap = QPixmap(qImage)
    return qPixmap

class LeashUI(QMainWindow):
    def __init__(self,parent=None):
        super(LeashUI,self).__init__(parent)
        self.ui=uic.loadUi("LeashMW.ui",self)
        self.data=SAXS.AttrDict({})
        self.ui.resize(1000,800)
        self.connect(self.ui.actionLoad_Calibration, SIGNAL("triggered()"),self.newFile)
        self.calschema=json.load(open(os.path.dirname(__file__)+os.sep+'schema.json')) 
        self.ui.treeWidgetCal.clear()
         
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        QShortcut(QKeySequence("Ctrl+O"), self, self.newFile)
    def newFile(self):
        self.filename=QFileDialog.getOpenFileName(self,directory="../doc")
        self.filefh=open(self.filename,"rw")
        try:
            self.cal=json.load(self.filefh)
            validate(self.cal,self.calschema)
        except ValueError as e:
            print "UI not json"
            dialog=QErrorMessage(self)
            dialog.showMessage(e.message)
            return
        except ValidationError as e:
            dialog=QErrorMessage(self)
            dialog.showMessage(e.message)
            return
        self.ui.treeWidgetCal.clear()
        self.buildcaltree(self.cal,self.ui.treeWidgetCal)
        self.loadmask()
        
    def loadmask(self):
        self.mask=SAXS.openmask(self.cal)
        image=nparrayToQPixmap(self.mask)
        self.data.qtmask=image
        maskscene=QGraphicsScene()
        maskscene.addPixmap(image)
        self.ui.graphicsViewMask.setScene(maskscene)
        self.ui.graphicsViewMask.show()
        self.resizemask() 
    def resizemask(self):
        self.ui.graphicsViewMask.fitInView(QRectF(self.data.qtmask.rect()),Qt.KeepAspectRatio)
        self.ui.graphicsViewMask.show()
      
    def buildcaltree(self,cal,tree):
        for key in cal:
            entry=QTreeWidgetItem(tree)
            entry.setText(0,key)
            if type(cal[key])is dict:
                self.buildcaltree(cal[key], entry)
            else:
                field=QTreeWidgetItem(entry)
                field.setText(0,str(cal[key]))
if __name__ == "__main__":
    app=QApplication(sys.argv)
    form=LeashUI()
    form.show()
    app.exec_()
        