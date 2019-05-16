 
 
from optparse import OptionParser
import re, os
from datetime import tzinfo, timedelta, datetime
import json, csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy import misc
import tables as tb
import hashlib, pickle
import re
from jsonschema import validate, ValidationError
import os
import io
from builtins import int
import path
import queue
from threading import Thread
from threading import Lock
#msilib import seems to cause an error on the cc01-cluster
#commented out by MB on Sept. 30th 15
#from msilib import Directory

def readtiff(imagepath):
    '''
    Read the tif header (#strings)
    '''
    f = open(imagepath, "rb")
    i=0
    data={"filename":os.path.basename(imagepath)}
  
    p = re.compile('[ -~]{4,100}')
    for line in f:
        for token in p.findall(line.decode('cp1252','ignore')):
            m=re.match(r"(\d+):(\d+):(\d+)\s+(\d+):(\d+):(\d+)", token)
            if m:
                 data['date']=datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), 
                                       int(m.group(4)), int(m.group(5)), int( m.group(6))
                                       ).isoformat()
            else:
                    m=re.match(r".+?(\w+)\s*[:=]\s*(.+)", token)
                    if m:
                        number=re.search("(\d+\.*\d*)\s+(\w+)", m.group(2))
                        if number:
                            
                            data[m.group(1)+" ["+number.group(2)+"]"]=float(number.group(1))
                           
                        else:
                            data[m.group(1)]={}
                            if re.match(r"^\s*\d+\s*$", m.group(2)):
                                data[m.group(1)]=int(m.group(2))
                            else:
                                data[m.group(1)]=m.group(2)
                    else:
                         
                        m=re.match(r"#\s*(.+?)([e\-\d\.]+)\s+([a-zA-Z]+)", token)
                        if m:
                            
                            data[m.group(1)+"["+m.group(3)+"]"]=float(m.group(2))
                           
                        else:
                            pass
                            #print token
                
        i+=1
        if i>20: break
    f.close()
    return data

def readlog(logfile):
    '''
    read CSV into pandas data frame
    '''
     
    dframe=pd.read_csv(logfile, sep="\t" )
    dframe[dframe.columns[0]]= (pd.to_datetime(dframe[dframe.columns[0]], unit="s"))
    dframe.reset_index()
    dframe=dframe.set_index(dframe.columns[0])
    return dframe

def imgtohdf(conf, imgdirectory, outputdirecory):
    '''
    add images in dir to hdf5 location
    '''
    filename=os.path.normpath(os.sep.join([os.path.normpath(outputdirecory),
                                       conf["OutputFileBaseName"]]))+".hdf"
    h5file = tb.open_file(filename, mode = "a", title = "Test file")
    #print "open: "+filename
    try:
        group=h5file.get_node("/", "Images")
    except tb.exceptions.NoSuchNodeError:
        group = h5file.create_group("/", 'Images', 'Dedector Images')
   
    for path, subdirs, files in os.walk(imgdirectory):
        for name in files:
            if name.endswith('tif'):
                imagefilename=os.path.join(path, name)
                data=misc.imread(imagefilename)
                imagefilename= imagefilename.split(".")[0]
                
                id="h"+hashlib.sha224(imagefilename.encode('utf-8')).hexdigest()
                try:
                    h5file.get_node("/Images", id)
                except tb.exceptions.NoSuchNodeError:
                    h5file.create_array(group, id, data,
                                   imagefilename)
    h5file.close()
    print("imgtohdf succeded")

def graphstohdf(conf, fileslist, outputdirecory):
    '''
    add images in dir to hdf5 location
    '''
    filename=os.path.normpath(os.sep.join([os.path.normpath(outputdirecory),
                                       conf["OutputFileBaseName"]]))+".hdf"
    h5file = tb.open_file(filename, mode = "a", title = "Test file")
    #print "open: "+filename
    #fileslist.to_csv('filelist.txt')
    try:
        group=h5file.get_node("/", "Graphs")
    except tb.exceptions.NoSuchNodeError:
        group = h5file.create_group("/", 'Graphs', 'Plotable Graphs')
    for kind in fileslist:
        try:
            h5file.get_node("/Graphs", kind)
        except tb.exceptions.NoSuchNodeError:
            h5file.create_group("/Graphs", kind,   kind)
       
        
        for graphfile in fileslist[kind]:
            
            if kind=="JSON":
                jsondata=json.load(open(graphfile, "r"))
                try:
                    imagefilename=graphfile.split(".")[0]
                except Exception as e:
                    continue      
            else:
                chifile=open(graphfile, "r").readlines()
                imagefilename= graphfile.split(".")[0]
            
            id="h"+hashlib.sha224(imagefilename.encode('utf-8')).hexdigest()
            try:
                node= h5file.get_node("/Graphs/"+kind, id)
            except tb.exceptions.NoSuchNodeError:
                node= h5file.create_group("/Graphs/"+kind, id,imagefilename)
            if kind=="JSON":
                h5file.create_array(node, "JSON", json.dumps(jsondata, indent=2).encode('utf-8'), "chifile" )
            else:
                h5file.create_array(node, "CHI", "".join(chifile).encode('utf-8'), "chifile" )
    h5file.close()


def readimglog(filename):
    """
    Read the log files the detector writes along with the images
    """
    logf=open(filename) 
    logfstr=""
    for i, line in enumerate(logf):
        if i==0:
            continue
        elif line.startswith("----"):
            continue
        elif len(line.split())<3:
             logfstr+="NaN NaN " +line
        else:
            logfstr+=line
    df=pd.read_csv(io.StringIO(logfstr), 
            sep=" ", 
            skipinitialspace=True,
            header=None, 
            names=["Time Requested", "Time Measured", "End Date Time", "File Name"],
            )
    df["End Date Time"]=pd.to_datetime(df["End Date Time"])
   
    return df

class merger_immagereader:
    def __init__(self, app, dir):
        self.frameinit=False
        self.tiffonly = False
        self.megestatus=""
        self.imgframe=pd.DataFrame()
        self.imagecount=0
        self.lock = Lock()
        
    def image_worker(self,img_queue):
        while True:
            imgpath = img_queue.get()
            row=readtiff(imgpath)
            row['filepath']=imgpath
            imgpath=imgpath.split(".")[0]
            row['id']="h"+hashlib.sha224(imgpath.encode('utf-8')).hexdigest()
            rowframe=pd.DataFrame()
            rowframe=rowframe.append(row, ignore_index=True)
            rowframe["date"]=pd.to_datetime(rowframe['date'])
            rowframe=rowframe.set_index(["date"])
            with self.lock:
                self.imgframe=imgframe.append(rowframe)
            img_queue.task_done()
        
    def readallimages(self):
        imglogframe=pd.DataFrame()
        chilist=[]
        '''starting image reader pool'''
        img_queue = Queue()
        thread_pool_size = 8
        for i in range(thread_pool_size):
            t = Thread(name="image_worker"+str(i), target=self.image_worker, args=(img_queue,))
            t.daemon= True
            t.start()
            
        
        for path, subdirs, files in os.walk(self.dir):
            if "Pil100k" in path:
                continue
            
            self.mergestatus= "\nSearching path: "+ path
            self.app.writeToMergeStatus(self.mergestatus)
            
            if "results" in path:
                self.tiffonly = True
            else:
                self.tiffonly = False
                
            for name in files:
                try:
                    if name.endswith('tif'):
                        img_queue.put(os.path.join(path, name))
                  
                    elif  name.endswith("log") and tiffonly == False:
                        logpath=os.path.join(path, name)
                        imglogframe=imglogframe.append(readimglog(logpath))
                    elif name.endswith("chi") or name.endswith("json") and tiffonly == False :
                        chilist.append(os.path.join(path, name))
                except:
                    print("error in ", imgpath)
                    mergestatus= "\nERROR in:"+ imgpath+"!!\nTry to keep going... Make sure to check the data once concluded!"
                    app.writeToMergeStatus(mergestatus)
        
        '''img_queue end'''
        img_queue.join()
        
        '''Adding identifier to column names'''
        imgframe.columns+=" (Img)"
        imglogframe.columns+=" (ImgLog)"
        
        '''Move date index into normal column'''
        imgframe["date (Img)"]=imgframe.index
        
        '''Make comparison column using'''
        imgframe["File Name (Img)"]=(imgframe["Image_path (Img)"]+imgframe['filename (Img)'])
        '''Merge by filepath+name'''
        merged=pd.merge(imglogframe, imgframe, 
                        left_on="File Name (ImgLog)",
                        right_on= "File Name (Img)",
                        how='right')
        
        '''Fill image time when no log information is present'''
        merged["End Date Time (ImgLog)"] = merged["End Date Time (ImgLog)"].fillna(merged["date (Img)"])
        merged["Time Measured (ImgLog)"] = merged["Time Measured (ImgLog)"].fillna(merged["Exposure_time [s] (Img)"])
        merged["End Date Time (ImgLog)"] = pd.to_datetime(merged["End Date Time (ImgLog)"])
        
        '''Adding a detector selector'''
        merged['Detector type']=""
        merged.loc[merged['File Name (Img)'].str.contains("Pil1M"), 'Detector type'] = "Pil1M"
        merged.loc[merged['File Name (Img)'].str.contains("Pil100k"), 'Detector type'] = "Pil100K"
            
        '''Adding 1ns offset for all 100K images, so no duplicate identifiers exist'''
        merged.loc[merged['Detector type']=="Pil100K", "End Date Time (ImgLog)"] = merged[merged['Detector type']=="Pil100K"]["End Date Time (ImgLog)"]+ timedelta(seconds=0.000001)
    
        merged = merged.set_index("End Date Time (ImgLog)")
        merged.sort_index(inplace=True)
           
        '''If some duplicate entries are left over, they are distinguished now'''
        index=[]
        index.append(merged.index[0])
        duplicateoffset=0.000001
        for pos in range(0, merged.index.shape[0]): 
            try : 
                if merged.index[pos+1] - merged.index[pos] < timedelta(seconds=0.000001) :
                    print("Duplicate found at pos: ", pos)
                    index.append(merged.index[pos+1] +timedelta(seconds=duplicateoffset))
                    duplicateoffset+=0.000001
                else:
                    index.append(merged.index[pos+1])
            except:
                break
        merged.index=index  
    
        '''Removing redundant columns'''
        merged = merged.drop('Time Requested (ImgLog)', 1)
        merged = merged.drop('File Name (ImgLog)', 1)
        
        '''Removing all 100K images'''
        merged = merged[merged['Detector type']!="Pil100K"]
        #if False:
        #    merged=imgframe
        
        mergestatus="\nDone going through all subfolders... A total of " + str(len(merged.index)) + " images were found."
        app.writeToMergeStatus(mergestatus)
        
        return merged, chilisttodict(chilist)
        
'''depreciated''' 
def readallimages(app, dir):
    """
    read header from all images and collect files list
    """
    frameinit=False
    tiffonly = False
    mergestatus=""
    imgframe=pd.DataFrame()
    imglogframe=pd.DataFrame()
    chilist=[]
    imagecount=0
    for path, subdirs, files in os.walk(dir):
        
        if "Pil100k" in path:
            continue
        
        mergestatus= "\nSearching path: "+ path
        app.writeToMergeStatus(mergestatus)
        
        if "results" in path:
            tiffonly = True
        else:
            tiffonly = False
            
        for name in files:
            try:
                if name.endswith('tif'):
                    imgpath=os.path.join(path, name)
                    #print(imgpath)
                    row=readtiff(imgpath)
                    row['filepath']=imgpath
                    imgpath=imgpath.split(".")[0]
                    row['id']="h"+hashlib.sha224(imgpath.encode('utf-8')).hexdigest()
                    rowframe=pd.DataFrame()
                    rowframe=rowframe.append(row, ignore_index=True)
                    rowframe["date"]=pd.to_datetime(rowframe['date'])
                    rowframe=rowframe.set_index(["date"])
                    imgframe=imgframe.append(rowframe)
              
                elif  name.endswith("log") and tiffonly == False:
                    logpath=os.path.join(path, name)
                    imglogframe=imglogframe.append(readimglog(logpath))
                elif name.endswith("chi") or name.endswith("json") and tiffonly == False :
                    chilist.append(os.path.join(path, name))
            except:
                print("error in ", imgpath)
                mergestatus= "\nERROR in:"+ imgpath+"!!\nTry to keep going... Make sure to check the data once concluded!"
                app.writeToMergeStatus(mergestatus)
    

    '''Adding identifier to column names'''
    imgframe.columns+=" (Img)"
    imglogframe.columns+=" (ImgLog)"
    
    '''Move date index into normal column'''
    imgframe["date (Img)"]=imgframe.index
    
    '''Make comparison column using'''
    imgframe["File Name (Img)"]=(imgframe["Image_path (Img)"]+imgframe['filename (Img)'])
    '''Merge by filepath+name'''
    merged=pd.merge(imglogframe, imgframe, 
                    left_on="File Name (ImgLog)",
                    right_on= "File Name (Img)",
                    how='right')
    
    '''Fill image time when no log information is present'''
    merged["End Date Time (ImgLog)"] = merged["End Date Time (ImgLog)"].fillna(merged["date (Img)"])
    merged["Time Measured (ImgLog)"] = merged["Time Measured (ImgLog)"].fillna(merged["Exposure_time [s] (Img)"])
    merged["End Date Time (ImgLog)"] = pd.to_datetime(merged["End Date Time (ImgLog)"])
    
    '''Adding a detector selector'''
    merged['Detector type']=""
    merged.loc[merged['File Name (Img)'].str.contains("Pil1M"), 'Detector type'] = "Pil1M"
    merged.loc[merged['File Name (Img)'].str.contains("Pil100k"), 'Detector type'] = "Pil100K"
        
    '''Adding 1ns offset for all 100K images, so no duplicate identifiers exist'''
    merged.loc[merged['Detector type']=="Pil100K", "End Date Time (ImgLog)"] = merged[merged['Detector type']=="Pil100K"]["End Date Time (ImgLog)"]+ timedelta(seconds=0.000001)

    merged = merged.set_index("End Date Time (ImgLog)")
    merged.sort_index(inplace=True)
       
    '''If some duplicate entries are left over, they are distinguished now'''
    index=[]
    index.append(merged.index[0])
    duplicateoffset=0.000001
    for pos in range(0, merged.index.shape[0]): 
        try : 
            if merged.index[pos+1] - merged.index[pos] < timedelta(seconds=0.000001) :
                print("Duplicate found at pos: ", pos)
                index.append(merged.index[pos+1] +timedelta(seconds=duplicateoffset))
                duplicateoffset+=0.000001
            else:
                index.append(merged.index[pos+1])
        except:
            break
    merged.index=index  

    '''Removing redundant columns'''
    merged = merged.drop('Time Requested (ImgLog)', 1)
    merged = merged.drop('File Name (ImgLog)', 1)
    
    '''Removing all 100K images'''
    merged = merged[merged['Detector type']!="Pil100K"]
    #if False:
    #    merged=imgframe
    
    mergestatus="\nDone going through all subfolders... A total of " + str(len(merged.index)) + " images were found."
    app.writeToMergeStatus(mergestatus)
    
    return merged, chilisttodict(chilist)
    
  
def compileconffromoptions(options, args):
    """
    If data merge is used as command line tool this compiles a json config according to 
    :ref:`consroot`
    
    """
    conf= {
     "TimeOffset": float(options.timeoffset), 
     "LogDataTables": [
       {
         "TimeOffset": 0.0, 
         "TimeEpoch":"Mac",
         "FirstImageCorrelation": options.syncfirst, 
         "ZeroImageCorrelation": options.synczero, 
         "Name": "Peak", 
         "Files": [
           {
             "RemotePath": [
                args[1]
             ],
            "LocalPath":""
           } 
         ]
       }, 
       {
         "TimeOffset": 0.0, 
    "TimeEpoch":"Mac",
         "FirstImageCorrelation": False, 
         "Name": "Dlog", 
         "Files": [
           {
             "RemotePath": [
               args[2]
             ],
            "LocalPath":""
           } 
           
         ]
       }
     ], 
     "OutputFormats": {
       "csv": False, 
       "hdf": False, 
       "exel": False, 
       "json": False
     }, 
     "OutputFileBaseName": ".//results//logs//", 
     "HDFOptions": {
       "IncludeCHI": options.includechi, 
       "IncludeTIF": options.includetifdata
     }
    } 
    suffix=options.outfile.split(".")[-1]
    knownoutput=False
    for format in conf["OutputFormats"]:
        if suffix=="xls":
            conf["OutputFormats"]["exel"]=True
            knownoutput=True
        if suffix==format:
            conf["OutputFormats"][format]=True
            knownoutput=True
    #print json.dumps(conf,  indent=2)
    if not knownoutput:
        print(options.outfile +": File format not supported.")
    return conf
def merge():
    '''saxs data merger'''
    
    parser = OptionParser()
    usage = "usage: %prog [options] iMPicture/dir peakinteg.log datalogger.log"
    parser = OptionParser(usage)
    parser.add_option("-t", "--timeoffset", dest="timeoffset",
                      help="Time offset between logging time and time in imagedata.", metavar="SEC", default=0)
    parser.add_option("-1", "--syncfirst", dest="syncfirst",
                      help="Sync time by taking the time difference between first shutter action and first image.", 
                      action="store_true", default=False)
    parser.add_option("-z", "--synczero", dest="synczero",
                      help="Sync time by taking the time difference between first shutter action and the zero.tif image.", 
                      action="store_true", default=False)
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="Write merged dataset to this file. Format is derived from the extesion.(.csv|.json|.hdf)", metavar="FILE", default="")
    parser.add_option("-b", "--batch", dest="batch",
                      help="Batch mode (no plot).", 
                       action="store_true", default=False)
    parser.add_option("-c", "--includechi", dest="includechi",
                      help="Include radial intensity data (.chi) in hdf.", 
                       action="store_true", default=False)
    parser.add_option("-f", "--includetif", dest="includetifdata",
                      help="Include  all image data in hdf.", 
                       action="store_true", default=False)
                     
    parser.add_option("-C", "--conf", dest="conffile",
                      help="Use config in  FILE to merge the data (ignore other options) ", metavar="FILE", default="")
  
    (options, args) = parser.parse_args(args=None, values=None)
    if len(args)<1:
         parser.error("Incorrect number of arguments. --help for more")
        
    if options.conffile!="":
        conf=json.load(open(options.conffile, "r"))
    else:
        conf=compileconffromoptions(options, args)

    directory=args[0]
    mergedTable, filelists, plotdata=mergedata(conf, directory)
    if not options.batch:
        plt.show()
    
    writeTable(conf, mergedTable)
    writeFileLists(conf, filelists)
    if conf["OutputFormats"]["hdf"] and conf['HDFOptions']["IncludeTIF"]:
        imgtohdf(conf, directory, ".")
    if conf["OutputFormats"]["hdf"] and conf['HDFOptions']["IncludeCHI"]:
        graphstohdf(conf, filelists, ".")
    
def writeTable(app,conf,mergedTable,directory="."):
    mergestatus=""
    basename=os.path.normpath(os.sep.join([os.path.normpath(directory), conf["OutputFileBaseName"]]))
    oldindex = mergedTable.index
    mergedTableTS=mergedTable
    mergedTableTS.index = (mergedTableTS.index-np.datetime64('1904-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    mergedTableTS.to_csv(basename+"_igor.csv")
    mergedTable.index = pd.to_datetime(oldindex)
    
    for format in conf["OutputFormats"]:
        if conf["OutputFormats"][format]:
           
            if format=="json":
                mergedTable.to_json(basename+"."+format)
            elif format=="csv":
                mergedTable.to_csv(basename+"."+format)
            elif  format=="exel":
                mergedTable.to_excel(basename+"."+"xls")
                format="xls"
            elif format=="hdf":
                try:
                    os.remove(basename+"."+"hdf")
                except:
                    pass
                mergedTable.to_hdf(basename+"."+"hdf", "LogData")
                
            mergestatus= "\nWrite: " + basename+"."+format
            app.writeToMergeStatus(mergestatus)
            
def writeFileLists(app,conf,filelists,directory=".",serverdir=""):
    mergestatus=""
    basename=os.path.normpath(os.sep.join([directory, conf["OutputFileBaseName"]]))
    for kind in filelists:
        texfilename= basename+kind+".txt"
        listfile=open(texfilename, "w")
        for filename in filelists[kind]:
            listfile.write(os.path.normpath(filename[len(serverdir):])+"\n")
        listfile.close()
    mergestatus+= "\nWrite: " +texfilename
    app.writeToMergeStatus(mergestatus)
    
    '''Writing logfile'''
    texfilename=basename+"consolidate_log.log"
    f = open(texfilename, "w")
    f.write(app.getMergeStatusProtocoll())
    f.close()

def cleanuplog(logframe, logTable):
    logframe.columns+=" ("+logTable["Name"]+")"
    logframe.index=logframe.index-timedelta(seconds=logTable["TimeOffset"])
    if logTable["TimeEpoch"]=="Mac":
       logframe.index=logframe.index-( datetime.fromtimestamp(0)-datetime(1904, 1, 1, 0, 0, 0))
       
def chilisttodict(chi):
    chidict={}
    for chifile in chi:
        if chifile.endswith(".chi"):
            parts=chifile.split("_c")
            if len(parts)==1:
                basename=chifile[:-4]
                typelabel="R"
            else:
                basename="_c".join(parts[:-1]).split(os.sep)[-1]
                saxdogpart=parts[-1]
                typelabel=saxdogpart[0]
                nummatch=re.match(r"(\w\d+)", saxdogpart)
                if nummatch:
                    typelabel=nummatch.group(1)
                    
               
            if basename not in chidict:
                chidict[basename]=[{typelabel:chifile}]
            else:
                chidict[basename].append({typelabel:chifile})
        else:
             basename=chifile[:-5]
             if basename not in chidict:
                chidict[basename]=[{"JSON":chifile}]
             else:
                chidict[basename].append({"JSON":chifile})
            
    filelists={}
    for basename in sorted(chidict.keys()):
            fileset= chidict[basename]
            for file in fileset :
                kind= list(file.keys())[0]
                if kind in  filelists :
                    filelists[kind].append(file[kind])
                else:
                    filelists[kind]=  [file[kind]]
    return filelists

def mergelogs(app,conf,attachment=None,directory="."):
    
    schema=json.load(open(os.path.dirname(__file__)
                        +os.sep+'DataConsolidationConf.json'))
    validate(conf, schema)
    
    if not "LogDataTables" in conf:
         conf["LogDataTables"]=[]
    tablea=None
    tableb=None
    firstImage=None
    zeroCorr = None
    mergestatus = ""
    for tnumber, logTable in enumerate(conf["LogDataTables"]):
        
        for filenum, logfile in enumerate(logTable["Files"]):
            if logfile["LocalPath"]=="":
                buffer=open(os.sep.join(logfile["RemotePath"]))
            elif attachment and json.loads(attachment[0].decode('utf-8'))["filename"]==logfile["LocalPath"]:
                buffer=io.StringIO(json.loads(attachment.pop(0).decode('utf-8'))["data"])
            else:
                pass
                buffer=open(logfile["LocalPath"])
            tmplog=readlog(buffer)
            if filenum==0:
                logframe=tmplog                    
            else:
                logframe=logframe.append(tmplog).sort_index()
        cleanuplog(logframe, logTable)
        basename=os.path.normpath(os.sep.join([os.path.normpath(directory), logTable["Name"]]))
        logframe.to_csv(basename+".csv")
        mergestatus= "\nMerged logfile can be found in: " +  (basename+".csv")
        app.writeToMergeStatus(mergestatus)        
        logframe.index=logframe.index-timedelta(seconds=conf["TimeOffset"])
            
        if logTable["FirstImageCorrelation"]:
            firstImage=logframe.index.min()
            peakframe=logframe
            print(firstImage)
            mergestatus="\nFirst image corresponds to peakInteg time: " + pd.to_datetime(firstImage).strftime("%a, %d %b %Y %H:%M:%S")
            app.writeToMergeStatus(mergestatus)
        elif logTable["Name"]=="Peak":
            peakframe=logframe
        elif isinstance(peakframe, type(None)):
            peakframe=logframe
            
        if logTable["ZeroImageCorrelation"]:
            zeroCorr=peakframe.index.min()
            print(zeroCorr)
            mergestatus="\nZero image corresponds to peakInteg time: " + pd.to_datetime(zeroCorr).strftime("%a, %d %b %Y %H:%M:%S")
            app.writeToMergeStatus(mergestatus)
            
        if tnumber >=1:
            tableb=logframe
            tablea=tablea.join(tableb, how='outer') 
        else:
            tablea=logframe
          
    tablea.sort_index(inplace=True) 
    tablea = tablea.fillna(method='ffill')
    
    return tablea, firstImage, zeroCorr, peakframe, basename

def mergedata(conf,dir,attachment=None):
    print("mergedata")
    logsTable, firstImage, zeroCorr, peakframe, logbasename=mergelogs(conf, attachment=attachment)
    imgreader = merger_immagereader()
    #imd, chi=readallimages(dir)
    imd, chi=imgreader.readallimages(dir)
    mergedt= mergeimgdata(logbasename, dir, logsTable, imd, firstImage=firstImage, zeroCorr=zeroCorr)
    syncplotdata=syncplot(peakframe, imd)
    return mergedt, chi, syncplotdata

def mergeimgdata(app,logbasename,dir,tablea,imd,firstImage=None,zeroCorr=None):
    mergestatus=""
    delta=timedelta(seconds=0)
    '''
    ZeroImage correlation looks for two consecutive Files with ExpT = 3.456 and ExpP 4.567    
    '''
    '''Subtracting exposure time from image time to get moment of acquisition start'''
    index=[]
    for pos in range(imd.index.shape[0]):    
            index.append(imd.index[pos]-timedelta(seconds=(imd["Time Measured (ImgLog)"][pos])))
    imd.index=index  
    
    '''If firstimagecorrelation is selected:'''
    if firstImage:
        delta=(imd.index.min()-firstImage)
        tablea.index=tablea.index+delta
        #peakframe.index=peakframe.index+delta
        mergestatus= "\nTime shift (FirstImage):" +str(delta)
        app.writeToMergeStatus(mergestatus)
        
    '''If ZeroImageCorrelation is selected:'''
    if zeroCorr:
        time_zeroframe = imd[imd.apply(lambda x: "zero_1M_00000.tif" in x['File Name (Img)'], axis=1)].index[0]
        delta = time_zeroframe - zeroCorr
        tablea.index=tablea.index+delta
        #peakframe.index=peakframe.index+delta
        mergestatus= "\nTime shift (ZeroImage):" +str(delta)
        app.writeToMergeStatus(mergestatus)

    '''Now time correlation has been made - adding half exposure for peakinteg interpolation'''
    index=[]
    for pos in range(imd.index.shape[0]):    
            index.append(imd.index[pos]+timedelta(seconds=(imd["Time Measured (ImgLog)"][pos]*0.5)))
    imd.index=index  


    basename=logbasename
    '''Joining image data and logs'''
    mergedt=imd.join(tablea, how="outer").interpolate(method="time") 
   
    
    '''Debugging Output
    basename=logbasename
    tableaTS=tablea
    tableaTS.index = (tableaTS.index-np.datetime64('1904-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    tableaTS.to_csv(basename+"_tablea_igor.csv")

    imdTS = imd
    imdTS.index = (imdTS.index-np.datetime64('1904-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    imdTS.to_csv(basename+"_imd_igor.csv") 
    '''
    
    #mergedt=imd.join(tablea,how="outer")
    
    '''Debugging Output
    mergedtTS=mergedt
    mergedtTS.index = (mergedtTS.index-np.datetime64('1904-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    mergedtTS.to_csv(basename+"_mergedt_igor.csv")
    '''
    
    #'''Now removing duplicate filenames'''
    #imd = imd.groupby(imd["File Name (ImgLog)"]).last()
    '''Joining image data and logs'''
    mergedt=imd.join(tablea, how="outer").interpolate(method="time")    
    #'''Now removing duplicate entries'''
    #mergedt = mergedt.groupby(mergedt.index).last()
    mergedt.to_csv(basename+"_mergedt.csv")
    
    column_startave = mergedt.columns.get_loc('Ioni         (Dlogger)')
    column_stopave = len(mergedt.columns)
    mergedt['time_ave']=np.NaN
    #mergedt['transm (Peak)']=np.NaN
    #mergedt['transm (DLogger)']=np.NaN
    
    offset = 0
    counter = 0
    write_thresh = 10.
    
    '''Turning off warnings for chained assignments'''
    pd.options.mode.chained_assignment = None  # default='warn'
    
    mergestatus= "\nStart of the interpolation.. this can take a while."
    app.writeToMergeStatus(mergestatus)
    
    for pos in range(0, imd.index.shape[0]): 
        if (float(counter)/float(imd.index.shape[0])*100.>write_thresh):
            mergestatus= "\n\t" + str(write_thresh) +"% done..."
            app.writeToMergeStatus(mergestatus)
            write_thresh+=10
        counter+=1
        mergedt_pos = mergedt.index.get_loc(imd.index[pos])
        exp_time = np.mean(mergedt["Time Measured (ImgLog)"][mergedt_pos])
        if exp_time>=5.:
            try : 
                if imd.index[pos+1] - imd.index[pos] < timedelta(seconds=exp_time):
                    if imd['Detector type'][pos+1]!=imd['Detector type'][pos+1]:
                        offset = 2
                else:
                    offset = 1
            except:
                offset = 1
                
            try:
                mergedt_pos_t_start = mergedt_pos + offset
                mergedt_pos_t_stop = mergedt.index.searchsorted(mergedt.index[mergedt_pos_t_start] + timedelta(seconds=exp_time))
                time_sum = np.array(mergedt.index[mergedt_pos_t_stop], dtype='datetime64[ns]') -\
                           np.array(mergedt.index[mergedt_pos_t_start], dtype='datetime64[ns]')
                time_sum_s = time_sum/ np.timedelta64(1, 's')
                mergedt['time_ave'][mergedt_pos]=time_sum_s
            except:
                print("End of file reached")
            
            for i in range (column_startave, column_stopave):
                try :
                    mergedt.ix[mergedt_pos, i]=np.sum(mergedt.ix[mergedt_pos_t_start:mergedt_pos_t_stop, i].values)/time_sum_s
                except :
                    print(i)
                    print(mergedt_pos)
                    print(mergedt_pos_t_start)
                    print(mergedt_pos_t_stop)
                    break
    
        #mergedt['transm (Peak)'][mergedt_pos]=np.abs(mergedt['Diode_avg (Peak)'][mergedt_pos]/mergedt['Ioni_avg (Peak)'][mergedt_pos])
        #mergedt['transm (DLogger)'][mergedt_pos]=np.abs(mergedt['Diode        (Dlogger)'][mergedt_pos]/mergedt['Ioni         (Dlogger)'][mergedt_pos])

    #mergedt.to_csv(basename+"mergedt_join_manint.csv")
    mergedt=mergedt[mergedt.index.isin(imd.index)]
    mergestatus= "\nEnd of the interpolation!"
    app.writeToMergeStatus(mergestatus)
    #mergedt.to_csv(basename+"mergedt_join_int_isin.csv")
    
    #mergedt=imd.join(tablea,how="outer").interpolate(method="zero")
    #mergedt=mergedt[mergedt.index.isin(imd.index)]
    
    return mergedt, delta
  
def syncplot(shiftedreduced, imd):
        imd['Exposure_time [s] (Img)'][:].plot(style="ro")  
        shiftedreduced['Duration (Peak)'][shiftedreduced['Duration (Peak)']>0].plot(style="x")
        plt.legend( ('Exposure from Images', 'Exposure from Shutter'))
        plt.xlabel("Time")
        plt.ylabel("Exosure Time [s]")
        plt.title("Corellation")
       
        data= {"Images":json.loads(pd.DataFrame(imd['Exposure_time [s] (Img)']).to_json(orient="index")),
                "Shutter":json.loads(pd.DataFrame(shiftedreduced['Duration (Peak)']).to_json(orient="index"))}
        
        
        return data
if __name__ == '__main__':
    merge()
   
