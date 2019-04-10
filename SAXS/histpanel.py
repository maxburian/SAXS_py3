from PyQt4 import  QtGui
from PyQt4 import  QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
import datetime
import matplotlib.dates as dates
from . import plotdatathread
import prettyplotlib as ppl
from prettyplotlib import brewer2mpl
import pandas as pd
from numpy import size, floor
class histpanel(QtGui.QWidget):
    def __init__(self, app):
        super(histpanel, self).__init__()
        self.layout = QtGui.QGridLayout()
        self.nimagesproc=0
        self.activatetools=True
        self.updateplot=True
        self.minframe="none"
        self.maxframe="all until now"
        self.setLayout(self.layout)
        
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas, 0, 0)
        
        self.IP0figure=plt.figure()
        self.IP0canvas=FigureCanvas(self.IP0figure)
        self.layout.addWidget(self.IP0canvas, 0, 1)
        
        self.IP1figure=plt.figure()
        self.IP1canvas=FigureCanvas(self.IP1figure)
        self.layout.addWidget(self.IP1canvas, 1, 0)
        
        self.IP2figure=plt.figure()
        self.IP2canvas=FigureCanvas(self.IP2figure)
        self.layout.addWidget(self.IP2canvas, 1, 1)
        
        self.histdata=[]
        self.mindate=datetime.datetime(1900, 1, 1, 1, 1, 1)
        self.maxdate=datetime.datetime(2222, 1, 1, 1, 1, 1)
        self.app=app
        
        self.framelimitlayout=QtGui.QHBoxLayout()
        self.integmaxframewdgt=QtGui.QSpinBox()
        self.framelimitlabel=QtGui.QLabel("Number of Frames to Show: ")
        self.framelimitlayout.addWidget(self.framelimitlabel)
        self.framelimitlayout.addWidget(self.integmaxframewdgt)
        self.integmaxframewdgt.setRange(0, 200000)
        self.integmaxframewdgt.setValue(1000)
        self.layout.addLayout(self.framelimitlayout, 2, 0)
        
        self.setminframelayout=QtGui.QHBoxLayout()
        self.setminframelabel=QtGui.QLabel("Select first frame to show: ")
        self.setminframecb=QtGui.QComboBox()
        self.setminframecb.addItem("none")
        self.setminframecb.setEnabled(False) 
        self.setminframelayout.addWidget(self.setminframelabel, stretch=2)
        self.setminframelayout.addWidget(self.setminframecb, stretch=4)
        self.keepind=False
        self.setminframecb.currentIndexChanged.connect(self.builtFrameListMax)
        self.layout.addLayout(self.setminframelayout, 3, 0)
        
        self.setmaxframelayout=QtGui.QHBoxLayout()
        self.setmaxframelabel=QtGui.QLabel("Select last frame to show: ")
        self.setmaxframecb=QtGui.QComboBox()
        self.setmaxframecb.addItem("all until now")
        self.setmaxframecb.setEnabled(False)
        self.setmaxframelayout.addWidget(self.setmaxframelabel, stretch=2)
        self.setmaxframelayout.addWidget(self.setmaxframecb, stretch=4)
        self.layout.addLayout(self.setmaxframelayout, 4, 0)
        
        self.toggleupdatebutton=QtGui.QPushButton("Stop auto update!")
        self.connect(self.toggleupdatebutton, QtCore.SIGNAL('clicked()'), self.toggleupdate)
        self.layout.addWidget(self.toggleupdatebutton, 2, 1)
        
        self.repltintegbutton=QtGui.QPushButton("Replot!")
        self.connect(self.repltintegbutton, QtCore.SIGNAL('clicked()'), self.plotIntegParam)
        self.layout.addWidget(self.repltintegbutton, 4, 1)
        
    def plot(self, datastr):
        data=json.loads(str(datastr))
        #if (self.app.tab.currentIndex()==2 ):
        if (2==2):
            if "history" in data["data"]:
                self.histdata=np.array(data["data"]["history"], dtype=np.float)
                self.timestep(data)
                if data["data"]["stat"]["images processed"]==self.nimagesproc:
                    self.activatetools=True
                else:
                    self.activatetools=False
                self.nimagesproc = data["data"]["stat"]["images processed"]
        if "IntegralParameters" in  data["data"]:
            self.tempdata=None
            self.drawIntegParam(data)
         
    def timestep(self, data):
        if isinstance(data, dict)==False:
            data = json.loads(data)
        timestamp=float(data["data"]["stat"]["time"])
        #if (self.app.tab.currentIndex()==2 ):
        if (2==2):
            self.figure.clf()
            ax=self.figure.add_subplot(111)
            self.figure.set_frameon(False)   
            ax.patch.set_alpha(0)         
            ax.set_xlabel("Time [s]")
            ax.set_ylabel("Image Count")
            histdata = self.histdata-np.ceil(timestamp)
            histdata = histdata[histdata>-100]
            x = np.linspace(-100,0,101)
            try:
                hist, edges = np.histogram(histdata, x)  
                ppl.bar(ax,np.linspace(-100,0,100),hist) 
                maximum = int(np.max(hist))
            except:
                maximum=1
            ax.set_xlim((-100, 0))
            ax.set_ylim((0, 1.2*maximum))
            if size(self.histdata)>100:
                speed = -100./(self.histdata[size(self.histdata)-101]-self.histdata[size(self.histdata)-1])
            else:
                speed = 0
            ax.set_title( str(data["data"]["stat"]['images processed'])+" frames processed @ approx. "+ str(int(speed)) + "fps")
            self.figure.tight_layout()
            self.canvas.draw()
            
    def drawIntegParam(self, data):
        lists=data["data"]['IntegralParameters']
        try:
            df=pd.DataFrame(lists[list(lists.keys())[0]]).set_index("time")
        except:
            print("Some indexing error... continue")
            return
        df.index=pd.to_datetime(df.index)
        length=len(df)
        df=df[max(length-int(1000000), 0):length]
        df['corrlength']=df['I1']/df['I2']        
        self.tempdata=df.sort_index()
        
        if self.tempdata['file'].str.contains('/')[0] == True :
            fslfound=True
        else:
            fslfound=False
        if self.tempdata['file'].str.contains(r'\\')[0] == True :
            bslfound=True
        else:
            bslfound=False
            
        if fslfound==True and bslfound==True :
            self.filelist = self.tempdata['file'].str.rsplit('/', n=1, expand=True)[1]
            if self.filelist.str.contains(r'\\')[0] == True :
                self.filelist = self.filelist.str.rsplit("\\", n=1, expand=True)[1]
        if fslfound==True and bslfound==False :
            self.filelist = self.tempdata['file'].str.rsplit('/', n=1, expand=True)[1]
        if fslfound==False and bslfound==True :
            self.filelist = self.tempdata['file'].str.rsplit("\\", n=1, expand=True)[1]  
        if fslfound==False and bslfound==False :
            print('SOMETHING WENT WRONG!!!')
        if (self.app.tab.currentIndex()==2 and self.updateplot==True):
            self.plotIntegParam()
        
        
    def plotIntegParam(self):
        framelimit=self.integmaxframewdgt.value()
        self.get_timeboundaries()
        df=self.tempdata[self.mindate:self.maxdate]
        df.to_pickle('./plotinteg_df.pickle')
        
        length=len(df)
        plotrange_min=max(length-int(framelimit)-1, 0)
        plotrange_max=length-1
        
        self.IP0figure.clf()
        ax=self.IP0figure.add_subplot(111)
        self.IP0figure.set_frameon(False) 
        ax.patch.set_alpha(0)
        ppl.plot(ax,df.index[plotrange_min:plotrange_max], df['I0'][plotrange_min:plotrange_max])
        ax.set_ylabel('integ.I(q)')
        ax.xaxis.set_minor_locator(plt.MaxNLocator(6))  
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M:%S'))  # hours and minutes
        ax.xaxis.set_major_locator(plt.MaxNLocator(2))  
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y')) 
        self.IP0figure.tight_layout()
        self.IP0canvas.draw()

        self.IP1figure.clf()
        ax=self.IP1figure.add_subplot(111)
        self.IP1figure.set_frameon(False)
        ax.patch.set_alpha(0)
        #df['I2'][max(length-int(framelimit)-1, 0):length-1].plot(ax=ax)
        ppl.plot(ax,df.index[plotrange_min:plotrange_max], df['I2'][plotrange_min:plotrange_max])
        ax.set_ylabel("Invariant")
        ax.xaxis.set_minor_locator(plt.MaxNLocator(6))  
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M:%S'))  # hours and minutes
        ax.xaxis.set_major_locator(plt.MaxNLocator(2))  
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))         
        self.IP1figure.tight_layout()
        self.IP1canvas.draw()
        
        self.IP2figure.clf()
        ax=self.IP2figure.add_subplot(111)
        self.IP2figure.set_frameon(False)
        ax.patch.set_alpha(0)
        #df['corrlength'][max(length-int(framelimit)-1, 0):length-1].plot(ax=ax, color='green')
        ppl.plot(ax,df.index[plotrange_min:plotrange_max], df['corrlength'][plotrange_min:plotrange_max])
        ax.set_ylabel("corr.length")
        ax.xaxis.set_minor_locator(plt.MaxNLocator(6))  
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M:%S'))  # hours and minutes
        ax.xaxis.set_major_locator(plt.MaxNLocator(2))  
        ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))   
        self.IP2figure.tight_layout()
        self.IP2canvas.draw()

    def builtFrameListMin(self):
        npfilelist = self.filelist.tolist()
        self.minframe=str(self.setminframecb.currentText())
        self.keepind=False
        self.setminframecb.clear()
        self.setminframecb.addItem("none")
        self.setminframecb.addItems(npfilelist)
        self.setminframecb.setCurrentIndex(self.setminframecb.findText(self.minframe))
        self.keepind=True

    def builtFrameListMax(self):
        if self.keepind==True:
            self.maxframe=str(self.setmaxframecb.currentText())
            self.minframe=str(self.setminframecb.currentText())
            if self.minframe !="none":
                npfilelist = self.filelist[self.filelist.index > self.filelist[self.filelist.str.contains(str(self.minframe))].index[0]].tolist()
            else: 
                npfilelist = self.filelist
            self.setmaxframecb.clear()
            self.setmaxframecb.addItems(npfilelist)
            self.setmaxframecb.addItem("all until now")
            self.setmaxframecb.setCurrentIndex(self.setmaxframecb.findText(self.maxframe))
        
    def get_timeboundaries(self):
        minframe=str(self.setminframecb.currentText())
        maxframe=str(self.setmaxframecb.currentText())
        if minframe != "none":
            self.mindate=self.filelist[self.filelist.str.contains(str(minframe))].index[0]
        else : 
            self.mindate=datetime.datetime(1900, 1, 1, 1, 1, 1)
        if maxframe != "all until now":
            self.maxdate=self.filelist[self.filelist.str.contains(str(maxframe))].index[0]
        else:
            self.maxdate=datetime.datetime(2222, 1, 1, 1, 1, 1)
    
    def toggleupdate(self):
        if "Stop" in str(self.toggleupdatebutton.text()):
            self.updateplot=False
            self.setmaxframecb.setEnabled(True)
            self.setminframecb.setEnabled(True)
            #self.holdminframe.setEnabled(True)
            #self.holdmaxframe.setEnabled(True)
            self.builtFrameListMin()
            self.builtFrameListMax()
            self.toggleupdatebutton.setText("Start auto update!")
        elif "Start" in str(self.toggleupdatebutton.text()):
            self.updateplot=True
            self.setmaxframecb.setEnabled(False)
            self.setminframecb.setEnabled(False)
            #self.holdminframe.setEnabled(False)
            #self.holdmaxframe.setEnabled(False)
            self.toggleupdatebutton.setText("Stop auto update!")   
        
                
                    
        