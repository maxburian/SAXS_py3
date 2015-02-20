from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
 
import json
from jsonschema import validate,ValidationError
import os,re

TYPE=QtCore.Qt.UserRole
ISENUM=QtCore.Qt.UserRole+1
ENUM  =  QtCore.Qt.UserRole+2
SUBSCHEMA=QtCore.Qt.UserRole+3
ISFILE=QtCore.Qt.UserRole+4
class calibtreemodel(QtGui.QStandardItemModel ):
    def __init__(self):
      super(calibtreemodel, self).__init__()
      self.calschema=json.load(open(os.path.dirname(__file__)+os.sep+'schema.json')) 
      
    def loadfile(self,filename):
        self.filename=filename
        try:
            self.calib=json.load(open(filename))
            validate(self.calib,self.calschema)
        except Exception as e:
             self.err=QtGui.QErrorMessage()
             self.err.showMessage(str(e))
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
            if key=="MaskFile":
                value.setData("true",role=ISFILE)
           
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
                        modelarrayvaue=QtGui.QStandardItem(str(arrayitem))
                        modelarrayvaue.setData(json.dumps(schema['properties'][key]["items"]),role=SUBSCHEMA)
                        item.appendRow([modelarrayitem,modelarrayvaue])
                        
                        
                else:
                    if key in input:
                       
                        value.setData(str(input[key]), role=QtCore.Qt.DisplayRole)
                    
                    elif "default" in schema['properties'][key]:
                        value.setData(str(schema['properties'][key]['default']), role=QtCore.Qt.DisplayRole)
                if "description"in schema['properties'][key]:
                    value.setToolTip(tooltip)
                 
                if 'enum' in schema['properties'][key]:
                  
                    value.setData(  True ,role=ISENUM)
                    value.setData(  json.dumps(schema['properties'][key] ['enum']) ,role=ENUM)
                else:
                     value.setData( False ,role=ISENUM)
               
                
                parent.setChild(row,1,value)
                if 'units' in schema['properties'][key]:
                    units=QtGui.QStandardItem(str(schema['properties'][key]['units']))
                    parent.setChild(row,2,units)  
            else:## is object
                if (("required" in  schema['properties'][key] 
                and not schema['properties'][key]['required']) 
                or not  "required" in  schema['properties'][key]):
                    
                    value.setCheckable(True)
                    if key in input:
                        value.setCheckState(2)
                    else:
                        value.setCheckState(0)
                    
                    value.setData("object",role=TYPE)
                    parent.setChild(row,1,value)
                if key in input: self.bulidfromjson(input[key], schema['properties'][key], item)
            row+=1     
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
     