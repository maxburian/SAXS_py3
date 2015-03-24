from PyQt4 import  QtGui
from PyQt4 import  QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import json
import matplotlib.pyplot as plt
class plotpanel(QtGui.QWidget):
    def __init__(self):
        super(plotpanel,self).__init__()
        self.layout =QtGui.QVBoxLayout()
        self.setLayout(self.layout )
         
        self.canvases=[]
        self.figures=[]
    def plot(self,datastr):
        data=json.loads(unicode(datastr))
        for maskindex,set in enumerate(data["data"]["array"]):
            if len(self.canvases)<=maskindex:
                self.figures.append(plt.figure())
                self.canvases.append(FigureCanvas(self.figures[maskindex]))
                self.layout.addWidget(self.canvases[maskindex])
            figure=self.figures[maskindex]
            figure.clf()
            ax=figure.add_subplot(111)
            ax.plot(set[0],set[1])
            self.canvases[maskindex].draw()
            print "plot "+str(maskindex)