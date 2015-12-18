from PyQt4 import  QtGui
from PyQt4 import  QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
import datetime
import plotdatathread
import prettyplotlib as ppl
from prettyplotlib import brewer2mpl
import pandas as pd
class histpanel(QtGui.QWidget):
    def __init__(self,app):
        super(histpanel,self).__init__()
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas,0,0)
        
        self.IP0figure=plt.figure()
        self.IP0canvas=FigureCanvas(self.IP0figure)
        self.layout.addWidget(self.IP0canvas,0,1)
        
        self.IP1figure=plt.figure()
        self.IP1canvas=FigureCanvas(self.IP1figure)
        self.layout.addWidget(self.IP1canvas,1,0)
        
        self.IP2figure=plt.figure()
        self.IP2canvas=FigureCanvas(self.IP2figure)
        self.layout.addWidget(self.IP2canvas,1,1)
        
        self.histdata=[]
        self.app=app
        
        self.integmaxframewdgt=QtGui.QSpinBox()
        self.framelimitlayout=QtGui.QHBoxLayout()
        self.framelimitlabel=QtGui.QLabel("Number of Frames to Show: ")
        self.framelimitlayout.addWidget(self.framelimitlabel)
        self.framelimitlayout.addWidget(self.integmaxframewdgt)
        self.integmaxframewdgt.setRange(0, 200000)
        self.integmaxframewdgt.setValue(100)
        
        self.repltintegbutton=QtGui.QPushButton("Replot!")
        self.framelimitlayout.addWidget(self.repltintegbutton)
        self.connect(self.repltintegbutton,QtCore.SIGNAL('clicked()'),self.plotIntegParam)
        self.layout.addLayout(self.framelimitlayout,2,0)
        
    def plot(self,datastr):
        if (self.app.tab.currentIndex()==2 ):
            data=json.loads(unicode(datastr))
            if "history" in data["data"]:
                self.histdata=np.array(data["data"]["history"],dtype=np.float)
                self.timestep(data)
            if "IntegralParameters" in  data["data"]:
                self.tempdata=None
                self.drawIntegParam(data)
         
    def timestep(self,data):
        if type(data)==QtCore.QString:
            data=json.loads(unicode(data))
        timestamp=float(data["data"]["stat"]["time"])
        if (self.app.tab.currentIndex()==2 ):
            self.figure.clf()
            ax=self.figure.add_subplot(111)
            self.figure.set_frameon(False)
            ax.patch.set_alpha(0)
            ax.set_xlabel("Time [s]")
            ax.set_ylabel("Image Count")
            ppl.hist(ax,self.histdata-np.ceil(timestamp),bins=100,range=(-100,0))
            ax.set_xlim((-100,0))
            tstr= datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            ax.set_title(tstr +", "+ str(data["data"]["stat"]['images processed'])+" Images Processed")
            self.canvas.draw()
            
    def drawIntegParam(self,data):
        lists=data["data"]['IntegralParameters']
        df=pd.DataFrame(lists[lists.keys()[0]]).set_index("time")
        df.index=pd.to_datetime(df.index)
        length=len(df)
        df=df[max(length-int(1000000),0):length]
        df['corrlength']=df['I1']/df['I2']        
        self.tempdata=df
        self.plotIntegParam()
        
        
    def plotIntegParam(self):
        framelimit=self.integmaxframewdgt.value()
        df=self.tempdata
        length=len(df)
        
        self.IP0figure.clf()
        ax=self.IP0figure.add_subplot(111)
        ax.patch.set_alpha(0)
        df[['I0','I1']][max(length-int(framelimit),0):length].plot(ax=ax, secondary_y=['I1'])
        ax.set_xlabel('time')
        ax.set_ylabel('integ.I(q)')
        ax.right_ax.set_ylabel('integ.I(q)*q')
        self.IP0canvas.draw()

        self.IP1figure.clf()
        ax=self.IP1figure.add_subplot(111)
        ax.patch.set_alpha(0)
        df['I2'][max(length-int(framelimit),0):length].plot(ax=ax)
        ax.set_xlabel("time")
        ax.set_ylabel("Invariant")
        self.IP1canvas.draw()
        
        self.IP2figure.clf()
        ax=self.IP2figure.add_subplot(111)
        ax.patch.set_alpha(0)
        df['corrlength'][max(length-int(framelimit),0):length].plot(ax=ax,color='green')
        ax.set_xlabel("time")
        ax.set_ylabel("corr.length")
        self.IP2canvas.draw()
    #    x=3
    #   self.plotthread=plotdatathread.plotthread(self)
    #  self.connect(self.plotthread,QtCore.SIGNAL("plotdata(QString)"),self.drawIntegParam)
        
        