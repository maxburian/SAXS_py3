 
 
from optparse import OptionParser
import re,os
from datetime import tzinfo, timedelta, datetime
import json,csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def readtiff(imagepath):
  
    f = open(imagepath, "r")
    i=0
    data={"filename":os.path.basename(imagepath)}
  
    p = re.compile('[ -~]{4,100}')
    for line in f:
        for token in p.findall(line):
            m=re.match("(\d+):(\d+):(\d+)\s+(\d+):(\d+):(\d+)", token)
            if m:
                 data['date']=datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), 
                                       int(m.group(4)), int(m.group(5)),int( m.group(6))
                                       ).isoformat()
            
             
            else:
                    m=re.match(".+?(\w+)\s*[:=]\s*(.+)",token)
                    if m:
                        number=re.search("(\d+\.*\d*)\s+(\w+)",m.group(2))
                        if number:
                            
                            data[m.group(1)+" ["+number.group(2)+"]"]=float(number.group(1))
                           
                        else:
                            data[m.group(1)]={}
                            if re.match("^\s*\d+\s*$",m.group(2)):
                                data[m.group(1)]=int(m.group(2))
                            else:
                                data[m.group(1)]=m.group(2)
                    else:
                         
                        m=re.match("#\s*(.+?)([e\-\d\.]+)\s+([a-zA-Z]+)",token)
                        if m:
                            
                            data[m.group(1)+"["+m.group(3)+"]"]=float(m.group(2))
                           
                        else:
                            pass
                            #print token
                
        i+=1
        if i>20: break
    return data
def readlog(logfile):
    file=open(logfile)
    dframe=pd.read_csv(logfile,sep="\t" )
    dframe[dframe.columns[0]]= pd.to_datetime(dframe[dframe.columns[0]],unit="s")-( datetime.fromtimestamp(0)-datetime(1904, 1, 1, 0,0,0))
    dframe.reset_index()
    dframe=dframe.set_index(dframe.columns[0])
    return dframe


def readallimages(dir):
    
    frame=pd.DataFrame()
    for path, subdirs, files in os.walk(dir):
        for name in files:
            if name.endswith('tif'):
                row=readtiff(os.path.join(path, name))
                frame=frame.append(row,ignore_index=True)
    return frame
def merge():
    parser = OptionParser()
    usage = "usage: %prog [options] iMPicture/dir peakinteg.log datalogger.log"
    parser = OptionParser(usage)
    parser.add_option("-t", "--timeoffset", dest="timeoffset",
                      help="Time offset between logging time and time in imagedata.", metavar="SEC",default=0)
    parser.add_option("-1", "--syncfirst", dest="syncfirst",
                      help="Sync time by taking the time difference between first shutter action and first image.", 
                      action="store_true",default=False)
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="Sync time by taking the time difference between first shutter action and first image.", metavar="FILE",default="")
    parser.add_option("-i", "--imagedata", dest="imagedata",
                      help=" Load image data from previously stored file (imgdata.pkl).", metavar="FILE",default="")
    parser.add_option("-b", "--batch", dest="batch",
                      help="Batch mode (no plot).", 
                       action="store_true",default=False)
    
    (options, args) = parser.parse_args(args=None, values=None)
    if len(args)<3:
        parser.error("incorrect number of arguments")
        sys.exit()
    means=readlog(args[1])
    datalogger=readlog(args[2]) 
    
    a=pd.concat([datalogger,means],join='outer').interpolate(method="zero",axis=0) 
    merged=a[ a.index.isin(means.index)]
    merged=merged[merged['Duration']>0]
    if options.imagedata=="":
        imagedata=readallimages(args[0])
        imagedata['Timestamp']=pd.to_datetime(imagedata['date'])
        imagedata=imagedata.reset_index()
        imd=imagedata.set_index("Timestamp") 
        
        imd.to_pickle("imgdata.pkl")
    else:
        imd=pd.read_pickle(options.imagedata)
 
    shifted=merged.copy()
    if options.syncfirst:
        shifted.index=merged.index- ( merged.index.min()-imd.index.min())
    if options.timeoffset!=0:
         shifted.index=shifted.index -timedelta(0,float(options.timeoffset))
    print shifted.index.min(), imd.index.min()
    if not options.batch:
        imd['Exposure_time [s]'][:].plot(style="ro")
        shifted['Duration'][:].plot(style="x")
        plt.show()
    mim=pd.concat([imd,shifted],join="outer",axis=1).drop('Wavelength [A]',axis=1)
    mima=mim.interpolate(kind="zero" )
    mima=mima[mima.index.isin(imd.index)]
    
    if options.outfile!="":
        if options.outfile.endswith(".json"):
            mima.to_json(options.outfile)
        elif options.outfile.endswith(".csv"):
            mima.to_csv(options.outfile)
        elif options.outfile.endswith(".hdf"):
            mima.to_hdf(options.outfile,"merged")
        else:
            print options.outfile +" format not supported"
  
    
    #print mima.to_json()
if __name__ == '__main__':
    merge()
   