from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
import json, os
from . import jsonschematreemodel as im
from .Leash import  initcommand
import ctypes
from . import maskfileui
from PyQt4.QtGui import QComboBox
from PyQt4.Qt import QMessageBox
from collections import OrderedDict
class calibEditDelegate(QtGui.QItemDelegate):
    def __init__(self,app,  parent=None):
        super(calibEditDelegate, self).__init__(parent)
        self.app=app
 

    def createEditor(self, parent, option, index):
        """
        special method of QItemDelegate class
        """
        try:
            subschema=json.loads(str(index.model().data(index, role=im.SUBSCHEMA)))
        except ValueError:
            return None
            
        type= str(index.model().data(index, role=im.TYPE))
        editablearray= str(index.model().data(index, role=im.ISEDITABLEARRAY))
        editortype=None
        if subschema.get("appinfo"):
            editortype= subschema.get("appinfo").get("editor")
        if "enum" in subschema:
            isenum="true"
            enum=subschema['enum']
        else:
            isenum="false"
        
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
        elif editablearray=="editablearray":
            arrayeditdialog=arrayediddialog(index, parent)
            return arrayeditdialog
        elif  type== "object" or type=="array" or type=="arrayitem" :
            return None
        elif isenum=="true":
            combobox = QtGui.QComboBox(parent)
            combobox.addItems(sorted( enum))
            return combobox
        elif editortype=="File":
            dirname= os.path.dirname(str(index.model().filename))
            filepicker=QtGui.QFileDialog(directory=dirname)
            filepicker.setMinimumSize(800, 500)
            filepicker.setFileMode(filepicker.ExistingFile)
            return filepicker
        elif editortype=="RemoteDir":
            return RemoteDirPicker(self.app, parent, index)
        elif editortype=="RemoteFile":
            return RemoteDirPicker(self.app, parent, index, showfiles=True)
        else:
            return QtGui.QItemDelegate.createEditor(self, parent, option,
                                              index)
     

    def commitAndCloseEditor(self):
        """
        special method of QItemDelegate class
        """
        editor = self.sender()
        if isinstance(editor, (QtGui.QTextEdit, QtGui.QLineEdit)):
            self.emit(QtCore.SIGNAL("commitData(QWidget*)"), editor)
            self.emit(QtCore.SIGNAL("closeEditor(QWidget*)"), editor)


    def setEditorData(self, editor, index):
        """
        special method of QItemDelegate class
        """
        subschema=json.loads(str(index.model().data(index, role=im.SUBSCHEMA)))
        type=subschema['type']
        editortype=None
        if subschema.get("appinfo"):
            editortype= subschema.get("appinfo").get("editor")
    
        if "enum" in subschema:
            isenum="true"
            enum=subschema['enum']
        else:
            isenum="false"
         
        text = index.model().data(index, QtCore.Qt.DisplayRole)
        
        if  type=="number":
            value = float(text)
            editor.setValue(value)
        elif type=="integer":
            value = int(text)
            editor.setValue(value)
               
        elif isenum=="true" or editortype=="RemoteDir" :
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
        subschema=json.loads(str(index.model().data(index, role=im.SUBSCHEMA)))
        type=subschema['type']
        editablearray= str(index.model().data(index, role=im.ISEDITABLEARRAY))
        editortype=None
        display=None
        if ("appinfo" in subschema 
        and "display" in subschema["appinfo"]):
            display=subschema["appinfo"]['display']
        if subschema.get("appinfo"):
            editortype= subschema.get("appinfo").get("editor")
        if "enum" in subschema:
            isenum="true"
            enum=subschema['enum']
        else:
            isenum="false"
        
        if type == "integer":
             model.setData(index, (editor.value()))
        elif type == "number":
            model.setData(index, (editor.value()))
        elif editablearray=="editablearray":
              
             model.setData(index, editor.currentText(), role=im.ACTION)
             model.setData(index, ( "add/remove item"))
        elif isenum=="true":
             model.setData(index, (editor.currentText()))
        elif editortype=="RemoteDir":
            model.setData(index, (editor.currentText()))
            myrow= index.row()
            parentitem=index.model().itemFromIndex(index.parent())
            for row in range(myrow+1, parentitem.rowCount()):
                model.setData(parentitem.child(row, 1).index(), ".")
        elif editortype=="File":
            files=editor.selectedFiles()
            if files:
                filename=str(files[0])
                
                
                model.setData(index, (filename.replace("\\", "/")))
                if display=="MaskFile":
                    myrow= index.row()
                    image= index.model().itemFromIndex(index.sibling(index.row(), 0 ).child(0, 1))
                    try:
                        pixmap=maskfileui.getMaskPixMapFromFile(filename).scaledToWidth(200)
                        image.setData(
                                      (pixmap), 
                                      role=QtCore.Qt.DecorationRole)
                    except Exception as e:
                        print(str(e))
                        ctypes.windll.user32.MessageBoxA(0, "There seems to be a problem with the mask. Check Fit2D!".encode('ascii'), "Mask File:".encode('ascii'), 0x0|0x30)
                        #self.errormessage.
        else:
            QtGui.QItemDelegate.setModelData(self, editor, model, index)
    
class   arrayediddialog(QtGui.QComboBox):
    def __init__(self, index, parent):
        super(arrayediddialog, self).__init__( parent )
        
        tarrayitem=index.model().itemFromIndex(index.sibling(index.row(), 0))
        actions=["Cancel", "Add New Item"]
        for row in range ( tarrayitem.rowCount()):
            actions.append("Delete Item "+str(row))
       
        self.addItems(actions)
 
class RemoteDirPicker(QtGui.QComboBox):
    def __init__(self,app,parent,index,showfiles=False):
          super(RemoteDirPicker, self).__init__( parent)
          myrow= index.row()
          parentitem=index.model().itemFromIndex(index.parent())
          dirs=[]
          for row in range(myrow):
              diritem= parentitem.child(row, 1)
              dirs.append(str(diritem.data( QtCore.Qt.DisplayRole)))
          argu=["listdir", os.sep.join(dirs)]
          result=json.loads(initcommand(app.options, argu, app.netconf))
          orderedresult = OrderedDict(sorted(result.items(), reverse=True))
          
          self.setMaxCount(5000)
          self.setMaxVisibleItems(5000)
          self.addItem(".")
          if 'dircontent' in result['data']:
              for  dir in  orderedresult['data']['dircontent']:
                  if dir['isdir'] or showfiles :
                    self.addItem(dir['path'])
                    
          
                    