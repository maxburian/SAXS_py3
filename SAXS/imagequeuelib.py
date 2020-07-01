# coding: utf8
from threading import Thread, current_thread, active_count
import threading

import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from .AddToQueue import addtoqueue
from scipy import misc
# import imageio
import os, sys
from PIL import Image, TiffImagePlugin
 
import numpy as np
from multiprocessing import Queue, Value
from .Subproccompatibility import Process
from queue import Empty, Full
import matplotlib.pyplot as plt
import zmq
import json
import time
from . import datamerge
#from SAXS.tifffile import   TiffFile 

lock = threading.Lock()
def funcworker(self, threadid):
   """
   Function for subprocesses
   """
   while self.stopflag.value==0: 
        try:
            try:
                picture = self.picturequeue.get(timeout=1)
            except KeyboardInterrupt:
                break
            except Empty:
                continue
            self.procimage(picture, threadid)
         
        except KeyboardInterrupt:
            pass 
        except Exception as e:
            print(e) 
   
def filler(queue, dir):
            filequeue=[] 
            print("Picturequeue filler: " + dir)
            
            for path, subdirs, files in os.walk(dir):
                for name in files:
                    if name.endswith('tif'):
                        queue.put(os.path.join(path, name))   
class imagequeue:
    """
    This class keeps a queue of images which may be worked on in threads.
    
    :param SAXS.calibration Cal: The SAXS Calibration to use for the processing
    :param optparser options: The object with the comandline options of the saxsdog
    :param list args: List of command line options
    
    """
    def __init__(self, Cals, options, directory, conf):
         
         self.pool=[]
         self.cals=Cals
         self.conf=conf
         self.options=options
         self.picturequeue=Queue()
         self.histqueue=Queue(maxsize=10000)
         self.plotdataqueue=Queue(maxsize=1)
         self.directory=directory
         self.allp=Value('i', 0)
         self.stopflag=Value('i', 0)
         self.dirwalker=None
         self.observer=None
         self.filelist_output = np.array(["filename", 0, 0, 0])
         if not options.plotwindow: 
              plt.switch_backend("Agg")
         self.fig=plt.figure()
         if  options.plotwindow: 
              plt.ion()
       
    def getlastdata(self):
          print("getdatata" + str(self.lastfile))
          return self.lastfile, self.lastdata
    
    def fillqueuewithexistingfiles(self):
        """
        Fill the queue with the list of images that is already there.
        """
       
        if self.options.walkdirinthreads:
            print("Using threaded Picturequeue filler")
            self.dirwalker=Thread(target=filler, args=(self.picturequeue, self.directory))
            self.dirwalker.start()
        else:
            print("Using non-threaded Picturequeue filler")
            filler(self.picturequeue, self.directory)
        
    def procimage(self, picture, threadid):
            filelist={}
            max = 1000
            data=[]
            integparams={}
            
            '''Setting output directory paths'''
            if self.options.outdir!="":
                basename=self.options.outdir+os.sep+('_'.join(picture.replace('./', '').split(os.sep))[:-3]).replace('/', "_")
                basename=basename.replace(':', '').replace('.', '')
            else:
                reldir=os.path.join(os.path.dirname(picture),
                                      self.options.relpath)
                if not os.path.isdir(reldir):
                    try:
                        os.mkdir(reldir)
                    except:
                        print("Problem creating WORK directory!!!")
                        return
                basename=os.path.join(reldir,
                                      os.path.basename(picture)[:-4])
             
            '''Check if image exists or we are in Gisaxs mode''' 
            skipfile=False    
            for calnum, cal in enumerate(self.cals):
                if self.options["OverwriteFiles"]==False:
                    if len(list(enumerate(self.cals)))==1 or calnum==0:
                        filename=basename
                    else:
                        filename=basename+"_c"+cal.kind[0]+str(calnum)
                    chifilename=filename+".chi"
                    if os.path.isfile(chifilename):
                        filelist[cal.kind+str(calnum)]=chifilename
                        skipfile=True
                        if self.options["livefilelist"] is not "xxx":
                            lock.acquire()
                            with open(self.options["livefilelist"], 'a') as f_handle:
                                file_path = os.path.normpath(chifilename)
                                file_path=str.split(str(file_path), str(os.path.split(self.options["watchdir"])[0]))[1]
                                output = file_path +", "+str(0)+ ", "+str(0)+", "+str(0)+"\n"
                                f_handle.write(output)
                                f_handle.close()
                            lock.release()
                
            '''Check if image can be opened'''
            imgChecker = False
            i = 0
            if skipfile==False:                  
                # print("[", threadid, "] open: ", picture) 
                while imgChecker is False:
                    try:
                        # print("[", threadid, "]try opening picture: ", picture)
                        # image=imageio.imread(picture)
                        image=misc.imread(picture)
                        # if image can be opened, set boolean to True
                        if image.shape == tuple(self.cals[0].config["Geometry"]["Imagesize"]):
                            #print("[", threadid,i, "]: ","Image Format is Good")  
                            imgChecker = True
                        else:
                            #print("[", threadid,i, "]: ","Image Shape: ", image.shape)
                            #print("[", threadid,i, "]: ","Required Shape: ", tuple(self..cals[0].config["Geometry"]["Imagesize"]))
                            #print("[", threadid,i, "]: ","image ", picture, " has wrong format.")  
                            imgChecker = False
                    except KeyboardInterrupt:
                        return
                    except Exception as e:
                        pass
                    #   print("[", threadid,i, "]: ","e: ", e)

                    # If both tests are passed, we can break the loop
                    if imgChecker == True:
                        break
                    else:
                        if i<max:
                            #print("[", threadid,i, "]: ", "Issues with ", picture, ", lets wait.", max-i, " s")
                            time.sleep(0.001)
                            i=i+1
                            continue
                        else:
                            print("[", threadid, "]: ", "Gave it ", max, " tries - skipping picture: ", picture)
                            print("[", threadid, "]: ", "Adding it back into the picture queue.")
                            try:
                                self.picturequeue.put(picture)
                            except Exception as e:
                                print("[", threadid, "]: ","Error was: ", e)
                            try:
                                image=misc.imread(picture)
                                print("[", threadid, "]: ","Image Shape: ", image.shape)
                                print("[", threadid, "]: ","Required Shape: ", tuple(self.cals[0].config["Geometry"]["Imagesize"]))
                            except Exception as e:
                                print("[", threadid, "]: ","Error was: ", e)
                            return
                            
            print("[", threadid, "]: ", picture, "took ", (i), "ms." ) 
                
                
            if skipfile == False:    
                imgMetaData=datamerge.readtiff(picture)
                if "date" in imgMetaData:
                    imgTime=imgMetaData["date"]
                else:
                    imgTime=""
            else:
                    imgTime=""  
            
            if skipfile==False:  
                for calnum,cal in enumerate(self.cals):
                    if self.options.GISAXSmode == True and calnum==0: #pass on GISAXSmode information to calibration.integratechi
                        continue
                    if len(list(enumerate(self.cals)))==1 or calnum==0:
                        filename=basename
                    else:
                        filename=basename+"_c"+cal.kind[0]+str(calnum)                
                    chifilename=filename+".chi"
                    filelist[cal.kind+str(calnum)]=chifilename
                    if not self.options.resume or not os.path.isfile(chifilename):
                        result=cal.integratechi(image, chifilename, picture)
                        # print("[", threadid, "]: ",chifilename, " has been integrated!")
                        result["Image"]=picture
                        if "Integparam" in result:
                            integparams[cal.kind[0]+str(calnum)]=result["Integparam"]                  
                        data.append(result)
                        if self.options["livefilelist"] is not "xxx":
                            lock.acquire()
                            with open(self.options["livefilelist"], 'a') as f_handle:
                                file_path = os.path.normpath(chifilename)
                                file_path=str.split(str(file_path), str(os.path.split(self.options["watchdir"])[0]))[1]
                                if "Integparam" in result:
                                    output = file_path +", "+str(result["Integparam"]["I0"])+ \
                                        ", "+str(result["Integparam"]["I1"])+", "+str(result["Integparam"]["I2"])+"\n"
                                else:
                                    output = file_path +", "+str(0)+ \
                                        ", "+str(0)+", "+str(0)+"\n"
                                f_handle.write(output)
                                f_handle.close()
                            lock.release()
                        if threadid==0 and self.options.plotwindow:
                            # this is a hack it really schould be a proper GUI
                           
                            cal.plot(image, fig=self.fig)
                            plt.draw()
                           
                                 
                    if self.options.writesvg:     
                        if not self.options.resume or not os.path.isfile(filename+'.svg'):
                             cal.plot(image, filename+".svg", fig=self.fig)
                    if self.options.writepng:
                         if not self.options.resume or not os.path.isfile(filename+'.svg'):
                              misc.imsave(filename+".png", image)
                    #if self.options.silent:
                    #    if np.mod(self.allp.value, 100)==0:
                    #        print("[", threadid, "] ", self.allp.value)
                    #else:
                    #    print("[", threadid, "] write: ", filename+".chi") 
            
            with self.allp.get_lock():
                self.allp.value+=1
                
            filelist["JSON"]=basename+".json"
            
            try:
                self.histqueue.put({"Time":float(time.time()),
                                "ImgTime":imgTime, 
                                "FileList":filelist,
                                "BaseName":basename,
                                "IntegralParameters":integparams}, block=False)
            except Full:
                print("Full")
            return basename, data
        
    def clearqueue(self):
        while self.histqueue.empty()==False:
                self.histqueue.get()
        print("History Queue cleared")

        
    def start(self):  
        """
        Start threads and directory observer.
        """
        #start threads
        
        for threadid in range(1, self.options.threads):
            print("start proc [", threadid, "]")
           
            worker=Process(target=funcworker, args=(self, threadid))
            worker.daemon=True
            self.pool.append(worker)
            worker.start() 
            #self.processimage(picture,options)
        self.starttime=time.time() 
        if self.options.watch:
            eventhandler=addtoqueue(self.picturequeue)
            self.observer = Observer()
            self.observer.schedule(eventhandler, self.args[0], recursive=True)
            self.observer.start()
        #We let the master process do some work because its useful for matplotlib.
        if not self.options.nowalk:
            self.fillqueuewithexistingfiles()
        if self.options.servermode:
             from .Leash import addauthentication
        try:
            while (self.options.servermode or 
                    (not self.picturequeue.empty()) 
                    or (self.dirwalker and self.dirwalker.is_alive() )
                    or self.options.watch): 
                    try:
                        picture = self.picturequeue.get(timeout=1)
                    except Empty:
                        continue
                    
        		    #in Case something goes wrong
                    try:
                        lastfile, data =self.procimage(picture, 0)
                    except:
                        continue                   

                    if self.options.servermode:
                        request={"command":"putplotdata","argument":{"data":{
                                "result":"plot","data":{"filename":lastfile,"graphs":data,
                                                        "stat":{}}
                                  }}}
                     
                        self.plotdataqueue.put(request)
                    if np.mod(self.allp.value, 100)==0:
                        self.timreport()
        except KeyboardInterrupt:
            pass
        
        self.stop()
        self.timreport()
        return self.allp.value, time.time()-self.starttime
    def stop(self):
        print("\n\nWaiting for the processes to terminate.")
        if self.observer:
            self.observer.stop()
            self.observer.observer.join(1)   
        
        
        self.stopflag.value=1
        for worker in self.pool:
            print("join worker")
            worker.join(1)
        if self.dirwalker:
            self.dirwalker.join(1)
        print("empty pic queue")
        while True:
            try:
                self.picturequeue.get(False)
            except Empty:
                break
        print("empty hist queue")
        while True:
            try:
                self.histqueue.get(False)
            except Empty:
                break
        print("empty plot queue")
        while True:
            try:
                self.plotdataqueue.get(False)
            except Empty:
                break
        if os.sys.platform!="win32":
            try:
                self.histqueue.close()
                self.plotdataqueue.close()
            except Exception as e:
                print(e)
    def timreport(self):
        tottime=time.time()-self.starttime
        count=self.allp.value
        #print count
        if count==0:
            print("We didn't do any pictures ")
        else:
            print("\n\nelapsed time: ", tottime)
            print("\nProcessed: ", count, " pic")
            print(" time per pic: ", tottime/count, "[s]")
            print(" pic per second: ", count/tottime, "[/s]")
        time.sleep(1)
        
