from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
 
import json,os
import calibtreemodel as im
class calibEditDelegate(QtGui.QItemDelegate):
    def __init__(self,  parent=None):
        super(calibEditDelegate, self).__init__(parent)

 

    def createEditor(self, parent, option, index):
        """
        special method of QItemDelegate class
        """
        try:
            subschema=json.loads(unicode(index.model().data(index,role=im.SUBSCHEMA).toString()))
            type=subschema['type']
            if "enum" in subschema:
                isenum="true"
                enum=subschema['enum']
            else:
                isenum="false"
            isfile=unicode(index.model().data(index,role=im.ISFILE).toString())
            if type == "integer":
                spinbox = QtGui.QSpinBox(parent)
                spinbox.setRange(-200000, 200000)
                spinbox.setSingleStep(1)
               
                spinbox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                return spinbox
            elif type == "number":
                spinbox = QtGui.QDoubleSpinBox(parent)
                spinbox.setRange(-200000, 200000)
                spinbox.setSingleStep(0.1)
                spinbox.setDecimals(4)
                spinbox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                return spinbox
            elif isenum=="true":
                combobox = QtGui.QComboBox(parent)
                combobox.addItems(sorted( enum))
                return combobox
            elif isfile=="true":
                dirname= os.path.dirname(unicode(index.model().filename))
                filepicker=QtGui.QFileDialog(directory=dirname)
                filepicker.setMinimumSize(800,500)
                filepicker.setFileMode(filepicker.ExistingFile)
                 
                return filepicker
          
            else:
                return QtGui.QItemDelegate.createEditor(self, parent, option,
                                                  index)
        except ValueError:
            pass

    def commitAndCloseEditor(self):
        """
        special method of QItemDelegate class
        """
        editor = self.sender()
        if isinstance(editor, (QtGui.QTextEdit, QtGui.QLineEdit)):
            self.emit(SIGNAL("commitData(QWidget*)"), editor)
            self.emit(SIGNAL("closeEditor(QWidget*)"), editor)


    def setEditorData(self, editor, index):
        """
        special method of QItemDelegate class
        """
        subschema=json.loads(unicode(index.model().data(index,role=im.SUBSCHEMA).toString()))
        type=subschema['type']
        if "enum" in subschema:
            isenum="true"
            enum=subschema['enum']
        else:
            isenum="false"
         
        text = index.model().data(index, QtCore.Qt.DisplayRole).toString()
        isfile=unicode(index.model().data(index,role=im.ISFILE).toString())
        if  type=="number":
            value = float(text)
            editor.setValue(value)
        elif type=="integer":
            value = int(text)
            editor.setValue(value)
               
        elif isenum=="true":
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)
        
            
        else:
            QtGui.QItemDelegate.setEditorData(self, editor, index)


    def setModelData(self, editor, model, index):
        """
        special method of QItemDelegate class
        """
        subschema=json.loads(unicode(index.model().data(index,role=im.SUBSCHEMA).toString()))
        type=subschema['type']
        if "enum" in subschema:
            isenum="true"
            enum=subschema['enum']
        else:
            isenum="false"
        isfile=unicode(index.model().data(index,role=im.ISFILE).toString())
        if type == "integer":
             model.setData(index, QtCore.QVariant(editor.value()))
        elif type == "number":
            model.setData(index, QtCore.QVariant(editor.value()))
        elif isenum=="true":
             model.setData(index, QtCore.QVariant(editor.currentText()))
        elif isfile=="true":
            files=editor.selectedFiles()
            if files:
                filename=unicode( files[0])
                dirname= os.path.dirname(unicode(index.model().filename))
                try:
                    relname=os.path.relpath(filename, dirname)
                except ValueError:
                    relname=filename
                
                model.setData(index,QtCore.QVariant(relname.replace("\\","/")))
        else:
            QtGui.QItemDelegate.setModelData(self, editor, model, index)
