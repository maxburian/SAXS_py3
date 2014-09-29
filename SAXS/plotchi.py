import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser

def parseopt():
    """
    Command line plotting tools for .chi files.
    """
    parser = OptionParser()
    usage = 'usage: %prog [options] CHIFILE [List of more ".chi" files]'
    parser = OptionParser(usage)
    
    parser.add_option("-o", "--out", dest="plotfile",
                      help="Write the plot to FILE. The format is derived from the suffix, e.g. '.svg','.pdf'."
                      , metavar="FILE",default="") 
    parser.add_option("-c", "--compare", dest="compare",
                      help="Compare datasets to first one."  , action="store_true",default=False) 
    parser.add_option("-l", "--log", dest="log",
                      help="Use log scale."  , action="store_true",default=False) 
    parser.add_option("-n", "--no-legend", dest="legend",
                      help="Hide legend."  , action="store_false",default=True) 
    parser.add_option("-t", "--title", dest="title",
                      help="Give plot title."
                      , metavar="TITLE",default="#filename") 
    parser.add_option("-s", "--skip", dest="skip",
                      help="Skip first N points."
                      , metavar="N",default=0 ,type="int")   
    parser.add_option("-k", "--clip", dest="clip",
                      help="Clip last N points." 
                      , metavar="N",default=1 ,type="int")
    parser.add_option("-x",'--xaxsistype',dest='xax',metavar='TYPE',default='linear',
                       help="Select type of X axis scale, might be [linear|log|symlog]")
    parser.add_option("-y",'--yaxsistype',dest='yax',metavar='TYPE',default='linear',
                       help="Select type of Y axis scale, might be [linear|log|symlog]")
    
     
    (options, args) = parser.parse_args(args=None, values=None)
    return  (options, args)
def plotchi():
    (options, args)= parseopt()
    makeplot(options, args)
    
def makeplot(options,args):
    set=0
    fig, ax1 = plt.subplots()
    for chifile in args:
        set+=1
        if options.compare:
            if set==1:
                first=np.loadtxt(chifile ,skiprows=4 )
                continue
            else:
                other=np.loadtxt(chifile ,skiprows=4 )
                data=np.array([
                                first[:,0] 
                                , 
                                np.interp(first[:,0], other[:,0],other[:,1])-first[:,1]
                               ]).transpose()
                ax1.plot(data[:,0],data[:,1],label=chifile)
                ax2=ax1.twinx()
                ax2.plot(data[:,0],data[:,1]/first[:,1]*100.0,label=chifile,color="g")
                ax2.set_ylabel('relative error %' ,color="g")
                align_yaxis(ax1,0,ax2,0)
        else:
            data=np.loadtxt(chifile ,skiprows=4 )
            ax1.plot(data[options.skip:-options.clip,0],data[options.skip:-options.clip,1],label=chifile)
          
            if data.shape[1]>=3:
 
                clipat=0.01
                ax1.fill_between( data[options.skip:-options.clip,0] ,
                   np.clip(data[options.skip:-options.clip,1]-data[options.skip:-options.clip,2],clipat,1e300),
                   np.clip(data[options.skip:-options.clip,1]+data[options.skip:-options.clip,2],clipat,1e300),
                   facecolor='blue' ,alpha=0.2,linewidth=0,label="Count Error")
                

        ax1.set_ylabel('Intensity [counts/pixel]')
        ax1.set_xlabel('q [1/nm]')
        plt.yscale(options.yax)
        plt.xscale(options.xax)
        if options.log: plt.yscale('log')
        
        plt.title(chifile)
    if options.title!="#filename":
             plt.title(options.title)
    if options.legend: ax1.legend( )
    if options.plotfile!="":
        plt.savefig(options.plotfile)
    else:
        plt.show()
    return plt
    
def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)    
    
if __name__ == '__main__':
    plotchi()