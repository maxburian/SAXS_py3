 
 
from optparse import OptionParser
import re,os
from datetime import tzinfo, timedelta, datetime
import json,csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy import misc
import tables as tb
import hashlib,pickle
import re
from jsonschema import validate,ValidationError
__file__="/home/chm/Dropbox/git/SAXS/SAXS/datamerge.py"
def readtiff(imagepath):
    '''
    Read the tif header (#strings)
    '''
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
    '''read CSV into pandas data frame'''
    file=open(logfile)
    dframe=pd.read_csv(logfile,sep="\t" )
    dframe[dframe.columns[0]]= pd.to_datetime(dframe[dframe.columns[0]],unit="s")-( datetime.fromtimestamp(0)-datetime(1904, 1, 1, 0,0,0))
    dframe.reset_index()
    dframe=dframe.set_index(dframe.columns[0])
    return dframe
def imgtohdf(path,dir):
    '''
    add images in dir to hdf5 location
    '''
    h5file = tb.open_file(path, mode = "a", title = "Test file")
    try:
        group=h5file.get_node("/", "Images")
    except tb.exceptions.NoSuchNodeError:
        group = h5file.create_group("/", 'Images', 'Dedector Images')
   
    for path, subdirs, files in os.walk(dir):
        for name in files:
            if name.endswith('tif'):
                imagefilename=os.path.join(path, name)
                data=misc.imread(imagefilename)
                
                id="h"+hashlib.sha224(imagefilename).hexdigest()
                try:
                    h5file.get_node("/Images", id)
                except tb.exceptions.NoSuchNodeError:
                    
                    h5file.createArray(group, id , data,
                                   imagefilename)
    h5file.close()
    
import os,hashlib


import StringIO

def readimglog(filename):
    logf=open(filename) 
    logfstr=""
    for i,line in enumerate(logf):
        if i==0:
            continue
        elif line.startswith("----"):
            continue
        elif len(line.split())<3:
             logfstr+="NaN NaN " +line
        else:
            logfstr+=line
    df=pd.read_csv( StringIO.StringIO(logfstr), 
            sep=" ", 
            skipinitialspace=True,
            header=None , 
            names=["Time Requested","Time Measured","End Date Time" ,"File Name"],
            )
    df["End Date Time"]=pd.to_datetime(df["End Date Time"])
   
    return df
 
def readallimages(dir):
    "read header from all images and collect chi files if required"
    frameinit=False
    imgframe=pd.DataFrame()
    imglogframe=pd.DataFrame()
    chilist=[]
    for path, subdirs, files in os.walk(dir):
        for name in files:
            if name.endswith('tif'):
                imgpath=os.path.join(path, name)
                row=readtiff(imgpath)
                row['filepath']=imgpath
                row['id']="h"+hashlib.sha224(imgpath).hexdigest()
                rowframe=pd.DataFrame()
             
                rowframe=rowframe.append(row,ignore_index=True)
                rowframe["date"]=pd.to_datetime(rowframe['date'])
                rowframe=rowframe.set_index(["date"])
                
                
                    
                imgframe=imgframe.append(rowframe)
              
            elif  name.endswith('log'):
                logpath=os.path.join(path, name)
                imglogframe=imglogframe.append(readimglog(logpath))
            elif name.endswith("chi"):
                chilist.append(os.path.join(path, name))
    imgframe["File Name"]=(imgframe["Image_path"]+imgframe['filename'])
    merged=pd.merge(imglogframe,imgframe, on="File Name")
    merged=merged.set_index("End Date Time")
    return merged,chilisttodict(chilist)
 
def merge():
    '''saxs data merger'''
    parser = OptionParser()
    usage = "usage: %prog [options] iMPicture/dir peakinteg.log datalogger.log"
    parser = OptionParser(usage)
    parser.add_option("-t", "--timeoffset", dest="timeoffset",
                      help="Time offset between logging time and time in imagedata.", metavar="SEC",default=0)
    parser.add_option("-1", "--syncfirst", dest="syncfirst",
                      help="Sync time by taking the time difference between first shutter action and first image.", 
                      action="store_true",default=False)
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="Write merged dataset to this file. Format is derived from the extesion.(.csv|.json|.hdf)", metavar="FILE",default="")
    parser.add_option("-i", "--imagedata", dest="imagedata",
                      help=" Load image data from previously stored file (imgdata.pkl).", metavar="FILE",default="")
    parser.add_option("-b", "--batch", dest="batch",
                      help="Batch mode (no plot).", 
                       action="store_true",default=False)
    parser.add_option("-c", "--includechi", dest="includechi",
                      help="Include radial intensity data (.chi) in hdf.", 
                       action="store_true",default=False)
    parser.add_option("-l", "--mergedlogfile", dest="mergedlogfile",
                      help="Write merged dataset to this file. The format is derived from the extesion.(.csv|.json|.hdf)", metavar="FILE",default="")
    parser.add_option("-f", "--includetif", dest="includetifdata",
                      help="Include  all image data in hdf.", 
                       action="store_true",default=False)
    (options, args) = parser.parse_args(args=None, values=None)
    if len(args)<3:
        parser.error("incorrect number of arguments")
        sys.exit()
    means=readlog(args[1])
    datalogger=readlog(args[2]) 
    merged=datalogger.join(means, how='outer').interpolate(method="zero") 
    mergedreduced=merged[merged.index.isin(means.index)]
    
    if options.imagedata=="":
        imd,chi=readallimages(args[0],options.includechi) 
        pickle.dump({"imd":imd,"chi":chi},open('imgdata.pkl',"w")) 
    else:
        dict=pickle.load(open(options.imagedata,"r"))
        imd=dict['imd']
        chi=dict['chi']
       
    shifted=merged.copy()
    shiftedreduced=mergedreduced.copy()
    # shift image timestamp py image exposure time
    index=[]
    for pos in range(imd.index.shape[0]):    
            index.append(imd.index[pos]-timedelta(seconds=imd['Exposure_time [s]'][pos]))
    imd.index=index   
    delta=timedelta(0)
    if options.syncfirst:
        delta=(  imd.index.min()- mergedreduced.index.min())
       
    if options.timeoffset!=0:
        delta=delta + timedelta(0,float(options.timeoffset))
    shifted.index=merged.index -delta
    shiftedreduced.index=mergedreduced.index  +delta
    shiftedreduced=shiftedreduced[shiftedreduced['Duration']>0]
    print "total timeshift: "+ str(delta.total_seconds()) +" Seconds"

    if not options.batch:
        imd['Exposure_time [s]'][:].plot(style="ro")
    
        shiftedreduced['Duration'][:].plot(style="x")
        plt.legend( ('Exposure from Images', 'Exposure from Shutter'))
        plt.xlabel("Time")
        plt.ylabel("Exosure Time [s]")
        plt.title("Corellation")
        plt.show()
     
    mim=shifted.join(imd,how="outer")
    mima=mim.interpolate(method="zero" )
    
    if options.mergedlogfile!="":
        if options.mergedlogfile.endswith(".json"):
            mima.to_json(options.mergedlogfile)
        elif options.mergedlogfile.endswith(".csv"):
            mima.to_csv(options.mergedlogfile)
        elif options.mergedlogfile.endswith(".hdf"):
            mima.to_hdf(options.mergedlogfile,"LogData")
           
            
        else:
            print options.mergedlogfile +" format not supported"
    
    mima=mima[mima.index.isin(imd.index)]
    
    if options.outfile!="":
        if options.outfile.endswith(".json"):
            mima.to_json(options.outfile)
        elif options.outfile.endswith(".csv"):
            mima.to_csv(options.outfile)
        elif options.outfile.endswith(".hdf"):
            mima.to_hdf(options.outfile,"Data")
            chi.to_hdf(options.outfile,"Curves")
            if options.includetifdata: imgtohdf(options.outfile,args[0])
        else:
            print options.outfile +" format not supported"
    else:
        print mima.to_string()
  
    
    #print mima.to_json()
    
def merge2():
    '''saxs data merger'''
    parser = OptionParser()
    usage = "usage: %prog [options] iMPicture/dir peakinteg.log datalogger.log"
    parser = OptionParser(usage)
    parser.add_option("-t", "--timeoffset", dest="timeoffset",
                      help="Time offset between logging time and time in imagedata.", metavar="SEC",default=0)
    parser.add_option("-1", "--syncfirst", dest="syncfirst",
                      help="Sync time by taking the time difference between first shutter action and first image.", 
                      action="store_true",default=False)
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="Write merged dataset to this file. Format is derived from the extesion.(.csv|.json|.hdf)", metavar="FILE",default="")
    parser.add_option("-i", "--imagedata", dest="imagedata",
                      help=" Load image data from previously stored file (imgdata.pkl).", metavar="FILE",default="")
    parser.add_option("-b", "--batch", dest="batch",
                      help="Batch mode (no plot).", 
                       action="store_true",default=False)
    parser.add_option("-c", "--includechi", dest="includechi",
                      help="Include radial intensity data (.chi) in hdf.", 
                       action="store_true",default=False)
    parser.add_option("-l", "--mergedlogfile", dest="mergedlogfile",
                      help="Write merged dataset to this file. The format is derived from the extesion.(.csv|.json|.hdf)", metavar="FILE",default="")
    parser.add_option("-f", "--includetif", dest="includetifdata",
                      help="Include  all image data in hdf.", 
                       action="store_true",default=False)
                     
    parser.add_option("-C", "--conf", dest="conffile",
                      help="use this json conf file to merge the data (ignore other options) ", metavar="FILE",default="")
  
    (options, args) = parser.parse_args(args=None, values=None)
    if options.conffile!="":
        conf=json.load(open(options.conffile,"r"))
    else:
        conf=compileconffromoptions(options, args)
    directory=args[0]
    mergedata(conf,directory)
def compileconffromoptions(options, args):
    pass
def cleanuplog(logframe,logTable):
    logframe.columns+=" ("+logTable["Name"]+")"
def chilisttodict(chi):
    chidict={}
    for chifile in chi:
        parts=chifile.split("_c")
        if len(parts)==1:
            basename=chifile[:-4]
            typelabel="R"
        else:
            basename="_c".join(parts[:-1]).split(os.sep)[-1]
            saxdogpart=parts[-1]
            typelabel=saxdogpart[0]
            nummatch=re.match(r"(\w\d+)",saxdogpart)
            if nummatch:
                typelabel=nummatch.group(1)
                
           
        if basename not in chidict:
            chidict[basename]=[{typelabel:chifile}]
        else:
            chidict[basename].append({typelabel:chifile})
    return chidict
def mergedata(conf,dir):
    schema=json.load(open(os.path.dirname(__file__)
                        +os.sep+'DataConsolidationConf.json'))
    validate(conf,schema)
    imd,chi=readallimages(dir)
    
    if not "LogDataTables" in conf:
         conf["LogDataTables"]=[]
    tablea=None
    tableb=None
    for tnumber,logTable in enumerate(conf["LogDataTables"]):
        
        for filenum ,logfile in enumerate(logTable["Files"]):
            
            tmplog=readlog(os.sep.join(logfile["Path"]))
            if filenum==0:
                logframe=tmplog
            else:
                logframe.append(tmplog)
        cleanuplog(logframe,logTable)
        
        if tnumber >=1:
            tableb=logframe
            tablea=tablea.join(tableb, how='outer') 
        else:
            tablea=logframe
    mergedt=imd.join(tablea,how="outer").interpolate(method="zero")
    mergedt=mergedt[mergedt.index.isin(imd.index)]
    return mergedt,chi
   