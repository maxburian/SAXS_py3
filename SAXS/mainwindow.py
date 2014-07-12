<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>718</width>
    <height>621</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Saxs Leash</string>
  </property>
  <widget class="QWidget" name="centralWidget">
   <layout class="QVBoxLayout" name="verticalLayout_8">
    <item>
     <widget class="QTabWidget" name="tabWidget">
      <property name="currentIndex">
       <number>1</number>
      </property>
      <widget class="QWidget" name="tab_Setup">
       <attribute name="title">
        <string>Setup</string>
       </attribute>
       <layout class="QVBoxLayout" name="verticalLayout_7">
        <item>
         <layout class="QGridLayout" name="gridLayout">
          <item row="4" column="0">
           <widget class="QCommandLinkButton" name="commandLinkButtonStartQueue">
            <property name="text">
             <string>Start Prosessing Queue With this Setup</string>
            </property>
           </widget>
          </item>
          <item row="2" column="0">
           <widget class="QGroupBox" name="groupBox">
            <property name="title">
             <string>Setup</string>
            </property>
            <layout class="QHBoxLayout" name="horizontalLayout_5">
             <item>
              <layout class="QHBoxLayout" name="horizontalLayout_2">
               <item>
                <widget class="QTreeWidget" name="treeWidgetCal">
                 <column>
                  <property name="text">
                   <string notr="true">Calibration</string>
                  </property>
                 </column>
                 <item>
                  <property name="text">
                   <string>Wavelength:</string>
                  </property>
                  <item>
                   <property name="text">
                    <string>1.5</string>
                   </property>
                  </item>
                 </item>
                 <item>
                  <property name="text">
                   <string>BeamCenter</string>
                  </property>
                  <item>
                   <property name="text">
                    <string>293</string>
                   </property>
                   <property name="flags">
                    <set>ItemIsSelectable|ItemIsEditable|ItemIsDragEnabled|ItemIsUserCheckable|ItemIsEnabled</set>
                   </property>
                  </item>
                  <item>
                   <property name="text">
                    <string>343</string>
                   </property>
                  </item>
                 </item>
                 <item>
                  <property name="text">
                   <string>Tilt</string>
                  </property>
                  <item>
                   <property name="text">
                    <string>TiltAngle</string>
                   </property>
                   <item>
                    <property name="text">
                     <string>3</string>
                    </property>
                   </item>
                  </item>
                  <item>
                   <property name="text">
                    <string>TiltRot</string>
                   </property>
                   <item>
                    <property name="text">
                     <string>34</string>
                    </property>
                   </item>
                  </item>
                 </item>
                </widget>
               </item>
               <item>
                <widget class="QGroupBox" name="groupBox_5">
                 <property name="title">
                  <string>Maskfile</string>
                 </property>
                 <layout class="QHBoxLayout" name="horizontalLayout_10">
                  <item>
                   <layout class="QVBoxLayout" name="verticalLayout_2">
                    <item>
                     <widget class="QPushButton" name="pushButtonLoadMask">
                      <property name="text">
                       <string>Load Maskfile</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget class="QGraphicsView" name="graphicsViewMask"/>
                    </item>
                   </layout>
                  </item>
                 </layout>
                </widget>
               </item>
              </layout>
             </item>
            </layout>
           </widget>
          </item>
          <item row="3" column="0">
           <widget class="QGroupBox" name="groupBox_2">
            <property name="title">
             <string>Directory</string>
            </property>
            <layout class="QHBoxLayout" name="horizontalLayout_4">
             <item>
              <layout class="QGridLayout" name="gridLayout_2">
               <item row="0" column="0">
                <widget class="QLabel" name="label_userdir">
                 <property name="text">
                  <string>User:</string>
                 </property>
                </widget>
               </item>
               <item row="1" column="1">
                <widget class="QLineEdit" name="lineEditExpDir"/>
               </item>
               <item row="0" column="1">
                <widget class="QLineEdit" name="lineEditUserDir"/>
               </item>
               <item row="2" column="1">
                <widget class="QLineEdit" name="lineEditSetupDir"/>
               </item>
               <item row="2" column="0">
                <widget class="QLabel" name="label_Setupdir">
                 <property name="text">
                  <string>Setup:</string>
                 </property>
                </widget>
               </item>
               <item row="1" column="0">
                <widget class="QLabel" name="label_Exdir">
                 <property name="text">
                  <string>Experiment:    </string>
                 </property>
                </widget>
               </item>
              </layout>
             </item>
            </layout>
           </widget>
          </item>
         </layout>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="tab_Plot">
       <attribute name="title">
        <string>Plot</string>
       </attribute>
       <layout class="QHBoxLayout" name="horizontalLayout_6">
        <item>
         <layout class="QVBoxLayout" name="verticalLayout">
          <item>
           <widget class="QGroupBox" name="groupBox_6">
            <property name="title">
             <string>Diffraction Curve</string>
            </property>
            <layout class="QHBoxLayout" name="horizontalLayout_11">
             <item>
              <layout class="QVBoxLayout" name="verticalLayout_3">
               <item>
                <widget class="QGraphicsView" name="graphicsViewPlot"/>
               </item>
               <item>
                <widget class="QLabel" name="label_Rate_2">
                 <property name="text">
                  <string>Rate:</string>
                 </property>
                </widget>
               </item>
               <item>
                <widget class="QLabel" name="label_File">
                 <property name="text">
                  <string>File:</string>
                 </property>
                </widget>
               </item>
              </layout>
             </item>
            </layout>
           </widget>
          </item>
         </layout>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="tabHistory">
       <attribute name="title">
        <string>History</string>
       </attribute>
       <layout class="QHBoxLayout" name="horizontalLayout_7">
        <item>
         <layout class="QVBoxLayout" name="verticalLayout_4">
          <item>
           <widget class="QGroupBox" name="groupBox_4">
            <property name="title">
             <string>Images Processed</string>
            </property>
            <layout class="QHBoxLayout" name="horizontalLayout_9">
             <item>
              <layout class="QVBoxLayout" name="verticalLayout_5">
               <item>
                <widget class="QGraphicsView" name="graphicsView_Hist"/>
               </item>
              </layout>
             </item>
            </layout>
           </widget>
          </item>
          <item>
           <widget class="QGroupBox" name="groupBox_3">
            <property name="title">
             <string>Meters</string>
            </property>
            <layout class="QHBoxLayout" name="horizontalLayout_8">
             <item>
              <layout class="QFormLayout" name="formLayout">
               <item row="0" column="0">
                <widget class="QLabel" name="label_TotFiles">
                 <property name="text">
                  <string>Files Processed</string>
                 </property>
                </widget>
               </item>
               <item row="2" column="0">
                <widget class="QLabel" name="label_Rate">
                 <property name="text">
                  <string>Current rate</string>
                 </property>
                </widget>
               </item>
               <item row="0" column="1">
                <widget class="QLCDNumber" name="lcdNumberFiles"/>
               </item>
               <item row="2" column="1">
                <widget class="QLCDNumber" name="lcdNumberRate"/>
               </item>
              </layout>
             </item>
            </layout>
           </widget>
          </item>
          <item>
           <widget class="QGroupBox" name="groupBox_7">
            <property name="title">
             <string>Logs</string>
            </property>
            <layout class="QHBoxLayout" name="horizontalLayout_12">
             <item>
              <layout class="QVBoxLayout" name="verticalLayout_6">
               <item>
                <widget class="QTextBrowser" name="textBrowserLogs">
                 <property name="html">
                  <string>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;lhksjdhfjkhh jsdhf &lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
                 </property>
                </widget>
               </item>
              </layout>
             </item>
            </layout>
           </widget>
          </item>
         </layout>
        </item>
       </layout>
      </widget>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menuBar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>718</width>
     <height>21</height>
    </rect>
   </property>
   <widget class="QMenu" name="menuSAXS_Leash">
    <property name="title">
     <string>&amp;File</string>
    </property>
    <addaction name="actionLoad_Calibration"/>
    <addaction name="actionSave_Calibration"/>
    <addaction name="actionImport"/>
    <addaction name="actionRecent_Files"/>
   </widget>
   <widget class="QMenu" name="menuQueue">
    <property name="title">
     <string>Queue</string>
    </property>
    <addaction name="actionClose_Queue"/>
    <addaction name="actionAbort_Queue"/>
   </widget>
   <widget class="QMenu" name="menuHelp">
    <property name="title">
     <string>Help</string>
    </property>
   </widget>
   <addaction name="menuSAXS_Leash"/>
   <addaction name="menuQueue"/>
   <addaction name="menuHelp"/>
  </widget>
  <widget class="QToolBar" name="mainToolBar">
   <attribute name="toolBarArea">
    <enum>TopToolBarArea</enum>
   </attribute>
   <attribute name="toolBarBreak">
    <bool>false</bool>
   </attribute>
  </widget>
  <widget class="QStatusBar" name="statusBar"/>
  <action name="actionLoad_Calibration">
   <property name="text">
    <string>&amp;Open Calibration</string>
   </property>
  </action>
  <action name="actionImport">
   <property name="text">
    <string>&amp;Import Calibration</string>
   </property>
  </action>
  <action name="actionClose_Queue">
   <property name="text">
    <string>Close Queue</string>
   </property>
  </action>
  <action name="actionAbort_Queue">
   <property name="text">
    <string>Abort Queue</string>
   </property>
  </action>
  <action name="actionSave_Calibration">
   <property name="text">
    <string>&amp;Save Calibration</string>
   </property>
  </action>
  <action name="actionRecent_Files">
   <property name="text">
    <string>Recent Files</string>
   </property>
  </action>
 </widget>
 <layoutdefault spacing="6" margin="11"/>
 <resources/>
 <connections/>
</ui>
