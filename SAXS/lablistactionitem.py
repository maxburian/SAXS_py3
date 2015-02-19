
import os
import platform
import sys,json
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class LablistActionItem(QWidget):
    def __init__(self,itemdata):
        super(LablistActionItem, self).__init__()
        self.expanded=False
        self.listlayout=QVBoxLayout()
        self.setLayout( self.listlayout)
        if "title" in itemdata:
            self.title=QPushButton()
            self.title.setStyleSheet ("""
            text-align: left;
             background-color:#BF574B; 
             font: bold 20px;  
             border-width: 0px;
             border-radius: 2px;
             margin:0px;
             padding: 6px;
             """); 
           
            self.title.setText(itemdata["title"])
            self.listlayout.addWidget(self.title)
        
        if "description" in itemdata:
            self.description=QLabel ()
            self.description.setWordWrap(True)
            self.description.setOpenExternalLinks(True);
            self.description.setText(itemdata["description"])
            self.listlayout.addWidget(self.description)
            self.connect(self.title, SIGNAL("pressed()"), self.toggleVisible)
            self.hide()
        
    def toggleVisible(self):
        if  self.description.isVisible():
            self.description.hide()
        else:
            self.description.show()
        