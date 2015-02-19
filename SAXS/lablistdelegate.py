from PyQt4.QtCore import *
from PyQt4.QtGui import *
import json,re,os
import lablistmodel as llm
 

class LabListtDelegate(QItemDelegate):
    def __init__(self):
      super(LabListtDelegate, self).__init__()
    def paint(self,painter,style,index):
        type= index.model().data(index,role=llm.TYPE).toString()
        data= index.model().data(index).toString()
        item= index.model().itemFromIndex(index)
      
        if type=="description":
            doc=QTextDocument()
            doc.setHtml(data)
            doc.setTextWidth(style.rect.width());
            style.text=""
            painter.translate(style.rect.left(), style.rect.top());
            clip=QRectF(0, 0, style.rect.width(), style.rect.height());
            doc.drawContents(painter,clip)
            painter.translate(-style.rect.left(), -style.rect.top());
            return
              
        QItemDelegate.paint(self, painter,style,index)
    def sizeHint(self,style,index):
        type= index.model().data(index,role=llm.TYPE).toString()
        data= index.model().data(index).toString()
        item= index.model().itemFromIndex(index)
      
        if type=="description":
            doc=QTextDocument()
            doc.setTextWidth(style.rect.width());
            doc.setHtml(data)
            doc.adjustSize()
            
            print "sizehint"
            print doc.idealWidth(), doc.size().height()
            return QSize(doc.idealWidth(), doc.size().height());
        return QItemDelegate.sizeHint(self,style,index) 
    def createEditor(self, parent, option, index):
        pass