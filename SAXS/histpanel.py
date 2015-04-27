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
import prettyplotlib as ppl
from prettyplotlib import brewer2mpl
class histpanel(QtGui.QWidget):
    def __init__(self,app):
        super(histpanel,self).__init__()
        self.layout =QtGui.QVBoxLayout()
        self.setLayout(self.layout )
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
   
        self.layout.addWidget(self.canvas)
        self.histdata=[]
        self.app=app
       
    def plot(self,datastr):
        data=json.loads(unicode(datastr))
        if "history" in data["data"]:
            self.histdata=np.array(data["data"]["history"])
            self.timestep(datastr)
         
    def timestep(self,resultstr):
        data=json.loads(unicode(resultstr))
        timestamp=data["data"]["stat"]["time"]
     
        if (   self.app.tab.currentIndex()==2 ):
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
         