from PyQt4.QtCore import *
from PyQt4.QtGui import  *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import json,os
import atrdict
import numpy as np
from Leash import initcommand
import time
class plotthread(QThread):
    """
    Thread to handle requesting data over the network and prepare 
    figures for displaying in  the main thread.
    """
    def __init__(self,mw):
        QThread.__init__(self)
        self.mw=mw
        self.mw.data.rate=np.zeros(100)
        self.mw.data.time=np.ones(100)
        self.mw.plotthreadgo=True
        self.yscale="symlog"
        self.ax = self.mw.figure.add_subplot(111)
        self.axhist=self.mw.figurehist.add_subplot(111)
        
    def setyscale(self,state):
        """
        On check state changed from y-scale check box widget
        """
        if state==0:
            self.yscale="linear"
        else:
            self.yscale="symlog"
        self.emit( SIGNAL('update(QString)'), "changed scale" )
    def run(self):
        """
        special method of Qtread subclass. this is caled when the .start() method is called to 
        initiate the thread.
        """
         
       
        try:       
            conf=json.load(open(os.path.expanduser("~"+os.sep+".saxsdognetwork")))
            argu=["plotdata"]
            o=atrdict.AttrDict({"server":""})
            result=initcommand(o,argu,conf)
            # discards the old graph
            
            # plot data
            object=json.loads(result)
            if object['result']=="Empty":
                pass
            else:
                 
            
                self.ax.cla()
                self.ax.set_ylabel('Intensity [counts/pixel]')
                self.ax.set_xlabel('q [1/nm]')
                data=np.array(object['data']['array']).transpose()
         
                data[data==0]=np.NaN
                skip=0
                clip=1
                clipat=0
                self.ax.plot(data[skip:-clip,0],data[skip:-clip,1])
                self.ax.fill_between( data[skip:-clip,0] ,
                                 np.clip(data[skip:-clip,1]-data[skip:-clip,2],clipat,1e300),
                                 np.clip(data[skip:-clip,1]+data[skip:-clip,2],clipat,1e300),
                                 facecolor='blue' ,alpha=0.2,linewidth=0,label="Count Error")
                self.ax.set_title(object['data']['filename'])
                self.ax.set_yscale(self.yscale)
         
                        
            
            self.axhist.cla() 
            self.axhist.set_ylabel('Rate [/s]')
            self.axhist.set_xlabel('Time [s]')
            self.mw.data.stat=object['data']["stat"]
            self.mw.data.rate[0]=self.mw.data.stat['pics']/self.mw.data.stat['time interval']
           
            self.mw.data.time[0]=self.mw.data.stat['time interval']+ self.mw.data.time[1]
           
            self.axhist.plot(self.mw.data.time,self.mw.data.rate,lw=2)
            self.axhist.fill_between(self.mw.data.time,0,self.mw.data.rate,alpha=0.4)
            self.axhist.set_ylim( [0,np.max([np.max(self.mw.data.rate),1])])
            self.axhist.set_xlim( [np.min(self.mw.data.time),np.max(self.mw.data.time)+1])
         
            self.mw.data.time=np.roll(self.mw.data.time,1)
            self.mw.data.rate=np.roll(self.mw.data.rate,1)
           
           
                # refresh canvas
        except Exception as e:
            print e
        self.emit( SIGNAL('update(QString)'), "data plotted" )
