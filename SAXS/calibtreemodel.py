from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
 
import json
from jsonschema import validate,ValidationError
import os,re
import collections
from schematools import schematodefault
TYPE=QtCore.Qt.UserRole
 
SUBSCHEMA=QtCore.Qt.UserRole+3
ISEDITABLEARRAY=QtCore.Qt.UserRole+5
ACTION=QtCore.Qt.UserRole+6
class calibtreemodel(QtGui.QStandardItemModel ):
    def __init__(self):
      super(calibtreemodel, self).__init__()
      self.calschema=json.load(open(os.path.dirname(__file__)+os.sep+'schema.json'),object_pairs_hook=collections.OrderedDict) 
      
      self.connect(self, QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'),self.handleitemchanged)
      
    def loadfile(self,filename):
        self.filename=filename
        try:
            self.calib=json.load(open(filename),object_pairs_hook=collections.OrderedDict)
            validate(self.calib,self.calschema)
        except Exception as e:
             self.err=QtGui.QErrorMessage()
             self.err.setWindowTitle("Schema Error")
             self.err.showMessage(str(e))
             return
        self.invisibleRootItem().setColumnCount(3)
        self.bulidfromjson(self.calib,self.calschema,self.invisibleRootItem())
    def bulidfromjson(self,  input, schema ,parent, row=0):
        """
        generate QStandardItem data structure from json file
        """
        for key in schema['properties']:
            
            if key=='comment':
                continue
      
            item=QtGui.QStandardItem(key)
            item.setColumnCount(3)
            if "description"in schema['properties'][key]:
                tooltip=  schema['properties'][key]['description']+"\n"
                tooltip=re.sub(":[a-zA-Z]+:", "", tooltip)
                if "default" in schema['properties'][key]:
                    tooltip+="\nDefault: " + str(schema['properties'][key]['default'])
                
                item.setToolTip(tooltip)
                
            
            parent.appendRow(item)
                
            value=QtGui.QStandardItem()
            value.setData(schema['properties'][key]['type'],role=TYPE)
            value.setData(json.dumps(schema['properties'][key]),role=SUBSCHEMA)
             
            if schema['properties'][key]['type']!="string":
                value.setData(QtCore.Qt.AlignRight,role=QtCore.Qt.TextAlignmentRole)
            if schema['properties'][key]['type']!="object":
                if   row%2==0:
                    value.setBackground(QtGui.QBrush(QtGui.QColor(179,215,178) ,style = QtCore.Qt.SolidPattern))
                else:
                    value.setBackground(QtGui.QBrush(QtGui.QColor(212,255,211) ,style = QtCore.Qt.SolidPattern))
                if schema['properties'][key]['type']=="boolean":
                    if key in input:
                        boolv=input[key]
                    else:
                        boolv=schema['properties'][key]["default"]
                    value.setCheckable(True)
                    if boolv :
                        value.setCheckState(2)
                    else:
                        value.setCheckState(0 )
                elif   schema['properties'][key]['type']=="array" and key in input :
                    for arrayindex,arrayitem in enumerate(input[key]):
                       
                        modelarrayitem=QtGui.QStandardItem(str(arrayindex))
                        modelarrayitem.setColumnCount(3)
                        modelarrayvalue=QtGui.QStandardItem()
                        modelarrayvalue.setData(json.dumps(schema['properties'][key]["items"]),role=SUBSCHEMA)
                        if (not "maxItems" in schema['properties'][key] or
                           schema['properties'][key]["maxItems"]!=schema['properties'][key]["minItems"] ):
                             value.setData("editablearray",role=ISEDITABLEARRAY)
                             value.setData("add/remove item",role=QtCore.Qt.DisplayRole)
                        modelarrayvalue.setData(schema['properties'][key]["items"]["type"],role=TYPE)
                        
                        modelarrayvalue.setData(QtCore.Qt.AlignRight,role=QtCore.Qt.TextAlignmentRole)
                        if schema['properties'][key]["items"]["type"]=="object":
                             modelarrayvalue.setData("arrayitem",role=TYPE)
                             item.appendRow([modelarrayitem,modelarrayvalue])
                             self.bulidfromjson(arrayitem, schema['properties'][key]["items"], modelarrayitem)
                        else:
                            modelarrayvalue.setData(str(arrayitem),role=QtCore.Qt.DisplayRole)
                           
                            item.appendRow([modelarrayitem ,modelarrayvalue])
                else:
                    if key in input:
                       
                        value.setData(str(input[key]), role=QtCore.Qt.DisplayRole)
                    
                    elif "default" in schema['properties'][key]:
                        value.setData(str(schema['properties'][key]['default']), role=QtCore.Qt.DisplayRole)
                if "description"in schema['properties'][key]:
                    value.setToolTip(tooltip)
             
                parent.setChild(row,1,value)
                if 'units' in schema['properties'][key]:
                    units=QtGui.QStandardItem(str(schema['properties'][key]['units']))
                    parent.setChild(row,2,units)  
            if schema['properties'][key]['type']=="object" or schema['properties'][key]['type']=="array":
                if (("required" in  schema['properties'][key] 
                and not schema['properties'][key]['required']) 
                or not  "required" in  schema['properties'][key]):
                    
                    value.setCheckable(True)
                    if key in input:
                        value.setCheckState(2)
                    else:
                        value.setCheckState(0)
                    
                   
                    parent.setChild(row,1,value)
                    print key
                if key in input and schema['properties'][key]['type']=="object":
                    value.setData("object",role=TYPE)
                    self.bulidfromjson(input[key], schema['properties'][key], item)
            row+=1     
    def handleitemchanged(self,index,index2):
        """
        generate json from QStandardItem data structure
        """
      
        if index.isValid() :
            parent=self.itemFromIndex(index.sibling(index.row(),0))
            item=self.itemFromIndex(index)
            type=item.data(role=TYPE).toString()
            text=item.data(role=QtCore.Qt.DisplayRole).toString()
            action=unicode(item.data(role=ACTION).toString())
            if not action:
                if  (item.isCheckable() 
                     and type=="object" 
                     and not item.hasChildren() 
                     and item.checkState()==2 ):
                    subschema=json.loads(unicode(item.data(role=SUBSCHEMA).toString()))
                    default=schematodefault(subschema)
                    self.dontsave=True
                    self.bulidfromjson(default, 
                                       subschema , 
                                       self.itemFromIndex(index.sibling(index.row(),0)),row=0 )
                    self.dontsave=False
                elif  (item.isCheckable() 
                       and type=="array" 
                       and not item.hasChildren() 
                       and item.checkState()==2):
                        value=self.itemFromIndex(index)
                        value.setData("editablearray",role=ISEDITABLEARRAY)
                        value.setData("add/remove item",role=QtCore.Qt.DisplayRole)
                        
                elif (item.isCheckable()   
                      and  parent.hasChildren() 
                      and item.checkState()==0):
                    if self.allowtodelete(parent):
                         
                        for row in range( parent.rowCount()+1):
                            parent.takeRow(0)
                       
                    else:
                        self.blockSignals(True)
                        item.setCheckState(2)
                        self.blockSignals(False)
            else:  
                if action=="Add New Item":
                    subschema=json.loads(unicode(item.data(role=SUBSCHEMA).toString()))['items']
                    self.setData(index,"",role=ACTION)
                    default=schematodefault(subschema)
                    print json.dumps(default,indent=2)
                    arrayroot=self.itemFromIndex(index.sibling(index.row(),0))
                    print arrayroot.rowCount()
                    nearrayitem=QtGui.QStandardItem(str(arrayroot.rowCount()))
                    value=QtGui.QStandardItem()
                    if subschema['type']!="object":
                        value.setData(subschema['type'],role=TYPE)
                        value.setData(json.dumps(subschema),role=SUBSCHEMA)
                        value.setData(subschema["default"],role=QtCore.Qt.DisplayRole)
                        if subschema['type']!="string":
                            value.setData(QtCore.Qt.AlignRight,role=QtCore.Qt.TextAlignmentRole)
                    else:
                        value.setData("arrayitem",role=TYPE)
                        self.bulidfromjson(default, 
                                     subschema , 
                                      nearrayitem,row=0 )
                    arrayroot.appendRow([nearrayitem,value])
                elif action.startswith("Delete Item"):
                    m=re.match("Delete Item (\d+)",action)
                    itemnumber=int(m.group(1))
                    arrayroot=self.itemFromIndex(index.sibling(index.row(),0))
                    arrayroot.removeRow(itemnumber)
                    
                    for row in range(arrayroot.rowCount()):
                        arrayroot.child(row,0).setData(str(row),role=QtCore.Qt.DisplayRole)
    def allowtodelete(self,parent):
        """
        Delete Dialog
        """
        text=parent.data(role=QtCore.Qt.DisplayRole).toString()
        dialog= QtGui.QDialog( )
        dialog.setWindowTitle("Delete "+text)
        buttons=QtGui.QDialogButtonBox( parent=dialog)
        delbutton=QtGui.QPushButton("Delete")
        buttons.addButton(delbutton, QtGui.QDialogButtonBox.AcceptRole)
        buttons.addButton( QtGui.QDialogButtonBox.Cancel)
        buttonlayout=QtGui.QHBoxLayout()
        buttonlayout.addWidget(buttons)
        vlayout=QtGui.QVBoxLayout()
        vlayout.addWidget(QtGui.QLabel("Do you really want to delete " +text))
        vlayout.addWidget(QtGui.QLabel("and all the items in it? "))
        vlayout.addWidget(QtGui.QLabel("Changes will be lost."))
        vlayout.addLayout(buttonlayout)

        dialog.setLayout(vlayout)
        self.connect(buttons, QtCore.SIGNAL("accepted()"), dialog, QtCore.SLOT("accept()"));
        self.connect(buttons, QtCore.SIGNAL("rejected()"), dialog, QtCore.SLOT("reject()"));
        dialog.exec_()
        return dialog.result()
    def save(self):
        print json.dumps(self.modeltojson(self.invisibleRootItem(), self.calschema),indent=2)
    def modeltojson(self, item, schema):
        """
        model to json converter recursive
        """
        js=collections.OrderedDict({})
        def stringtotype(type,value,item):
            if  type=="number":
                 value=float(value)
            elif type=="integer":
                 value=int(value)
            elif type=="boolean":
                if item.child(childrow,1).checkState():
                   value=True
                else:
                    value=False
            elif type=="object":
                pass
            elif type=="string":
                value= value
            else:
                pass
            return value
        type=None
        for childrow in range(item.rowCount()):
            child= item.child(childrow,0)
            name= unicode(child.data(role=QtCore.Qt.DisplayRole).toString())
            
            if item.child(childrow,1):
                type=unicode(item.child(childrow,1).data(role=TYPE).toString())
                value=unicode(item.child(childrow,1).data(role=QtCore.Qt.DisplayRole).toString())
            else: value=None
          
                
            if type and  (type=="array" ):
                    js[name]=[]
                    print type + " " +name+"# "+str(child.rowCount())
                    for arrayitemrow in range(child.rowCount()):
                        arrayitemlabel=child.child(arrayitemrow,0)
                        arrayitem=child.child(arrayitemrow,1)
                        if arrayitemlabel and arrayitem :
                            arraytype=unicode(arrayitem.data(role=TYPE).toString())
                            print arraytype
                            arrayvalue=unicode(arrayitem.data(role=QtCore.Qt.DisplayRole).toString())
                            if arraytype=="arrayitem":
                                js[name].append(self.modeltojson(child.child(arrayitemrow,0), schema))
                            else:
                                js[name].append(stringtotype(arraytype,arrayvalue,arrayitem))
            elif child.hasChildren():
                    js[name]=self.modeltojson(child, schema)
            else:
                js[name]=stringtotype(type,value,item)
        return js
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """
        special class of QStandardItemModel
        """
        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant(int(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter))
            return QtCore.QVariant(int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter))
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return QtCore.QVariant("Name")
            elif section == 1:
                return QtCore.QVariant("Value")
            elif section == 2:
                return QtCore.QVariant("Units")
            
        return QtCore.QVariant(int(section + 1))
    def flags(self, index):
        """
        special class of QStandardItemModel
        """
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column()==1:
            return QtCore.Qt.ItemFlags(QtGui.QStandardItemModel.flags(self, index)
                    |QtCore.Qt.ItemIsEditable)
        else:
            return QtCore.Qt.ItemFlags(QtGui.QStandardItemModel.flags(self, index)
                    ^QtCore.Qt.ItemIsEditable)