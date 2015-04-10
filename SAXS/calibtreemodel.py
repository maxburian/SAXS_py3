from PyQt4 import  QtGui
from PyQt4 import  uic
from PyQt4 import  QtCore
 
import json,base64
from jsonschema import validate,ValidationError
import os,re
import collections
from schematools import schematodefault
import maskfileui
TYPE=QtCore.Qt.UserRole
 
SUBSCHEMA=QtCore.Qt.UserRole+3
ISEDITABLEARRAY=QtCore.Qt.UserRole+5
ACTION=QtCore.Qt.UserRole+6
class calibtreemodel(QtGui.QStandardItemModel ):
    def __init__(self,app):
      super(calibtreemodel, self).__init__()
      self.app=app
      self.calschema=json.load(open(os.path.dirname(__file__)+os.sep+'schema.json'),object_pairs_hook=collections.OrderedDict) 
      self.connect(self, QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'),self.handleitemchanged)
      self.errormessage=QtGui.QErrorMessage()
      self.errormessage.setWindowTitle("Data Structure Error")
      self.filename=None
      self.calib=None
    def ifNoneInitFromDefault(self):
        if self.calib==None:
            self.InitFromDefault()
    def InitFromDefault(self):
        self.calib=schematodefault(self.calschema)
    def loadfile(self,filename):
        try:
            self.calib=json.load(open(filename),object_pairs_hook=collections.OrderedDict)
            validate(self.calib,self.calschema)
        except Exception as e:
             self.err=QtGui.QErrorMessage()
             self.err.setWindowTitle("Schema Error")
             self.err.showMessage(str(e))
             return
        self.filename=filename
        self.emit(QtCore.SIGNAL("fileNameChanged()"))
        self.app.statusmodified()
        self.blockSignals(True)
        self.clear()
        self.bulidfromjson(self.calib,self.calschema,self.invisibleRootItem())
        self.blockSignals(False)
    def loadservercalib(self,servercalib):
        self.calib=servercalib["data"]["cal"]
        self.filename=None
     
        for attachnr,attachment in enumerate( servercalib["data"]["attachments"]):
            if os.path.isfile(attachment['filename']):
                msgBox=QtGui.QMessageBox()
                msgBox.setText("'"+attachment['filename']+"' already exists")
                msgBox.setInformativeText("Do you want to replace it with the server version?")
                msgBox.setStandardButtons(msgBox.Ok |  msgBox.Retry| msgBox.Cancel)
                msgBox.setDefaultButton(msgBox.Ok)
                msgBox.setButtonText(msgBox.Ok,"Replace With Server Version")
                msgBox.setButtonText(msgBox.Retry,"Save As")
                msgBox.setButtonText(msgBox.Cancel,"Use Local Version")
                val=msgBox.exec_()
                if val==msgBox.Cancel:
                    continue
                elif val==msgBox.Retry:
                  
                    filedialog=QtGui.QFileDialog()
                    filename=unicode(filedialog.getSaveFileName(parent=None, caption="Save Mask File As"))
                    attachment['filename']=filename
                    self.calib["Masks"][attachnr]["MaskFile"]=filename
            print "write mask"
            maskfile=open(attachment['filename'],"wb")
            maskfile.write(base64.b64decode(attachment['data']))
            maskfile.close()
          
        print "load new"  
        self.clear()
        self.blockSignals(True)
        self.bulidfromjson(self.calib,self.calschema,self.invisibleRootItem())
        self.blockSignals(False)
        
    def rebuildModel(self):
        self.clear()
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
                        if ("appinfo" in schema['properties'][key]
                            and "display" in schema['properties'][key]["appinfo"]):
                            display=schema['properties'][key]["appinfo"]['display']
                            if display=="MaskFile":
                                maskimage=QtGui.QStandardItem()
                                image=QtGui.QStandardItem()
                                item.appendRow([maskimage ,image])
                                try:
                                    pixmap=maskfileui.getMaskPixMapFromFile(input[key]).scaledToWidth(200)
                                    image.setData(
                                              QtCore.QVariant(pixmap) , 
                                              role=QtCore.Qt.DecorationRole)
                                    
                                except Exception as e :
                                    print e
                                    pass
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
    def getjson(self):
        data=self.modeltojson(self.invisibleRootItem())
        print json.dumps(data,indent=2)
        try:
            validate(data,self.calschema)
        except Exception as e:
            self.errormessage.showMessage(str(e))
        return data
    def save(self):
        data=self.getjson()
        if not self.filename:
             dialog=QtGui.QFileDialog()
             self.filename= unicode(dialog.getSaveFileName(None,"Save File As"))
        json.dump(data,open(self.filename,"w"),indent=2)
        self.emit(QtCore.SIGNAL("fileNameChanged()"))
    def saveAs(self):
        dialog=QtGui.QFileDialog()
        self.filename= unicode(dialog.getSaveFileName(None,"Save File As"))
        
        self.save()
    def modeltojson(self, item):
        """
        model to json converter recursive
        """
        js=collections.OrderedDict({})
        def stringtotype(typestr,value,item):
            if  typestr=="number":
                 value=float(value)
            elif typestr=="integer":
                 value=int(value)
            elif typestr=="boolean":
                if item.child(childrow,1).checkState():
                   value=True
                else:
                    value=False
            elif typestr=="object":
                pass
            elif typestr=="string":
                value= value
            else:
                pass
            return value
        
      
        for childrow in range(item.rowCount()):
            child= item.child(childrow,0)
            name= unicode(child.data(role=QtCore.Qt.DisplayRole).toString())
            
            if item.child(childrow,1):
                valueitem=item.child(childrow,1)
                type=unicode(item.child(childrow,1).data(role=TYPE).toString())
                value=unicode(item.child(childrow,1).data(role=QtCore.Qt.DisplayRole).toString())
            else:
                print "##### "+name
                continue
            
            print name+":"+type
            
            if type and  (type=="array" ):
                    if valueitem.isCheckable() and valueitem.checkState()==0:
                        continue
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
                                js[name].append(self.modeltojson(child.child(arrayitemrow,0)))
                            else:
                                js[name].append(stringtotype(arraytype,arrayvalue,arrayitem))
            elif child.hasChildren() and type=="object":
                    js[name]=self.modeltojson(child)

            elif type!="object":
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