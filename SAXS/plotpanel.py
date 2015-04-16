# coding: utf8
from PyQt4 import  QtGui
from PyQt4 import  QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import json
import matplotlib.pyplot as plt
import prettyplotlib as ppl
 
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
        if  "data" in data and "graphs" in data["data"]:
            graphdata= data["data"]["graphs"]
            if len(graphdata)<len(self.canvases):
                for i in reversed(range(self.layout.count())): 
                    self.layout.itemAt(i).widget().deleteLater()
                
                self.canvases=[]
                self.figures=[]
            for maskindex,set in enumerate(graphdata):
                if len(self.canvases)<=maskindex:
                    self.figures.append(plt.figure( ))
                    self.canvases.append(FigureCanvas(self.figures[maskindex]))
                    self.layout.addWidget(self.canvases[maskindex])
                figure=self.figures[maskindex]
                figure.clf()
                figure.set_frameon(False)
               
                ax=figure.add_subplot(111)
                ax.set_yscale('symlog')
                ax.set_xlabel(set["columnLabels"][0])
                ax.set_ylabel(set["columnLabels"][1])
                ax.set_title( set["kind"]+" "+data["data"]['filename'])
                ax.patch.set_alpha(0)
                nonzero=np.array(set["array"][1])>0
                x=np.array(set["array"][0])[:]
                
                y=np.array(set["array"][1])[:]
                e=np.array(set["array"][2])[:]
                ppl.plot(ax,x,y,lw=1.0)
                ppl.fill_between(ax,x,y-e,y+e)
                self.canvases[maskindex].draw()
               