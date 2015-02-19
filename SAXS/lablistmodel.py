from PyQt4.QtCore import *
from PyQt4.QtGui import *
import json,os
TYPE=Qt.UserRole
class LabListModel( QStandardItemModel ):
     def __init__(self):
        super(LabListModel, self).__init__()
        self.root=self.invisibleRootItem()
        self.items={}
        self.sections={}
     
        
        for item in self.checklist:
            self.additem(item)
     def additem(self,item):
        title=QStandardItem(item["title"])
        self.sections[item["title"]]=title
        title.setSizeHint(QSize(0,50))
        description=QStandardItem( item["description"])
        description.setData("description",TYPE)
     
        title.appendRow( description )
    
        title.setBackground(QBrush(QColor(200,40,40)))
        self.root.appendRow(title)