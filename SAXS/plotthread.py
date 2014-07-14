from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
 
class plotthread(QObject):
 
    def plot(self,ui):
        if not ui.plotthread:
            ui.plotthreadgo=True
            
            ui.figure = plt.figure()
            ui.plotcanvas= FigureCanvas(ui.figure)
            ui.toolbar = NavigationToolbar(ui.plotcanvas, self)
            ui.ui.verticalLayout_3.addWidget(ui.toolbar)
            ui.ui.verticalLayout_3.addWidget(ui.plotcanvas)
                
            
               
            while ui.plotthreadgo:
                    conf=json.load(open(os.path.expanduser("~"+os.sep+".saxdognetwork")))
                    argu=["plotdata"]
                    o=SAXS.AttrDict({"server":""})
                    result=initcommand(o,argu,conf)
                     
                    ax = ui.figure.add_subplot(111)
                    # discards the old graph
                    ax.hold(False)
                    # plot data
                    object=json.loads(result)
                    print result
                    data=np.array(object['data']['array']).transpose()
                    skip=0
                    clip=1
                    clipat=0
                    ax.plot(data[skip:-clip,0],data[skip:-clip,1])
                    ax.fill_between( data[skip:-clip,0] ,
                                     np.clip(data[skip:-clip,1]-data[skip:-clip,2],clipat,1e300),
                                     np.clip(data[skip:-clip,1]+data[skip:-clip,2],clipat,1e300),
                                     facecolor='blue' ,alpha=0.2,linewidth=0,label="Count Error")
                    #ui.figure.title(object['data']['filename'])
                    ax.set_ylabel('Intensity [counts/pixel]')
                    ax.set_xlabel('q [1/nm]')
                    
                    # refresh canvas
                    ui.plotcanvas.draw()
           