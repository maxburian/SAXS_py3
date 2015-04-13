# coding: utf8
from PyQt4 import  QtGui
from PyQt4 import  QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import json
import matplotlib.pyplot as plt
import prettyplotlib as ppl
import matplotlib as mpl 
from prettyplotlib import brewer2mpl
import numpy as np
class plotpanel(QtGui.QWidget):
    def __init__(self):
        super(plotpanel,self).__init__()
        
        #self.setWidget(self.widget)
        self.layout =QtGui.QVBoxLayout()
        self.setLayout(self.layout )
        self.canvases=[]
        self.figures=[]
    def plot(self,datastr):
        data=json.loads(unicode(datastr))
        if  "data" in data and "array" in data["data"]:
            arraydata=np.array(data["data"]["array"])
            if len(arraydata)<len(self.canvases):
                for i in reversed(range(self.layout.count())): 
                    self.layout.itemAt(i).widget().deleteLater()
                
                self.canvases=[]
                self.figures=[]
            for maskindex,set in enumerate(arraydata):
                if len(self.canvases)<=maskindex:
                    self.figures.append(plt.figure( ))
                    self.canvases.append(FigureCanvas(self.figures[maskindex]))
                    self.layout.addWidget(self.canvases[maskindex])
                figure=self.figures[maskindex]
                figure.clf()
                figure.set_frameon(False)
               
                ax=figure.add_subplot(111)
                ax.set_yscale('symlog')
                ax.set_xlabel(u"Scattering Vector  θ")
                ax.set_ylabel("Intensity (Count/Pixel)")
                ax.set_title("Mask "+str(maskindex)+", "+data["data"]['filename'])
                ax.patch.set_alpha(0)
                nonzero=set[1]>0
                x=set[0][nonzero]
                y=set[1][nonzero]
                e=set[2][nonzero]
                ppl.plot(ax,x,y,lw=1.0)
                ppl.fill_between(ax,x,y-e,y+e)
                self.canvases[maskindex].draw()
                print "plot "+str(maskindex)