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
        self.layout =QtGui.QVBoxLayout()
        self.setLayout(self.layout )
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
   
        self.layout.addWidget(self.canvas)
        self.IPfigure=plt.figure()
        self.IPcanvas=FigureCanvas(self.figure)
        self.layout.addWidget(self.IPcanvas)
        self.histdata=[]
        self.app=app
        self.integmaxframewdgt=QtGui.QSpinBox()
       
        self.framelimitlayout=QtGui.QHBoxLayout()
        self.framelimitlabel=QtGui.QLabel("Number of Frames to Show: ")
        self.framelimitlayout.addWidget( self.framelimitlabel)
        self.framelimitlayout.addWidget(self.integmaxframewdgt)
        self.integmaxframewdgt.setRange(0, 200000)
        self.integmaxframewdgt.setValue(100)
        # self.repltintegbutton=QtGui.QPushButton("Replot!")
        # self.framelimitlayout.addWidget(self.repltintegbutton)
        # self.connect(self.repltintegbutton,QtCore.SIGNAL('clicked()'),self.replotIntegParam)
        self.layout.addLayout(self.framelimitlayout)
    def plot(self,datastr):
        if (self.app.tab.currentIndex()==2 ):
            data=json.loads(unicode(datastr))
            if "history" in data["data"]:
                self.histdata=np.array(data["data"]["history"],dtype=np.float)
                self.timestep(data)
            if "IntegralParameters" in  data["data"]:
                self.drawIntegParam(data)
         
    def timestep(self,data):
        if type(data)==QtCore.QString:
            data=json.loads(unicode(data))
        timestamp=float(data["data"]["stat"]["time"])
        print timestamp
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
        self.IPfigure.clf()
        ax=self.figure.add_subplot(111)
        ax.patch.set_alpha(0)
        lists=data["data"]['IntegralParameters']
        framelimit=self.integmaxframewdgt.value()
        df=pd.DataFrame(lists[lists.keys()[0]]).set_index("time")
        df.index=pd.to_datetime(df.index)
        length=len(df)
       
        df[max(length-int(framelimit),0):length].plot(ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title("Integral Parameters")

        self.IPcanvas.draw()
        
    # def replotIntegParam(self):
    #    x=3
    #   self.plotthread=plotdatathread.plotthread(self)
    #  self.connect(self.plotthread,QtCore.SIGNAL("plotdata(QString)"),self.drawIntegParam)
        
        