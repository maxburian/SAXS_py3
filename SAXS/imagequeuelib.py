from threading import Thread,current_thread,active_count

import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from AddToQueue import addtoqueue
from scipy import misc
import os,sys
from PIL import Image,TiffImagePlugin
from multiprocessing import Process
import numpy as np
from multiprocessing import Queue ,Value
from Queue import Empty
import matplotlib.pyplot as plt
import zmq
import json
#from SAXS.tifffile import   TiffFile 
def funcworker(self,threadid):
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
            self.procimage(picture,threadid)
        except KeyboardInterrupt:
            pass 
def filler(queue,dir):
            filequeue=[] 
            print "filler" + dir
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
    def __init__(self,Cal,options,args,conf):
         
         self.pool=[]
         self.cal=Cal
         self.conf=conf
         self.options=options
         self.picturequeue=Queue()
         self.args=args
         self.allp=Value('i',0)
         self.stopflag=Value('i',0)
         self.dirwalker=False
         if not options.plotwindow: 
              plt.switch_backend("Agg")
         self.fig=plt.figure()
         if  options.plotwindow: 
              plt.ion()
       
    def getlastdata(self):
          print "getdatata" + str(self.lastfile)
          return self.lastfile,self.lastdata
    
    def fillqueuewithexistingfiles(self):
        """
        Fill the queue with the list of images that is already there.
        """
       
                
        if self.options.walkdirinthreads:
            self.dirwalker=Process(target=filler,args=(self.picturequeue,self.args[0]))
            self.dirwalker.start()
        else:
            self.dirwalker=Process()
            self.dirwalker.start()
            filler(self.picturequeue,self.args[0])
        
    def procimage(self,picture,threadid):
       
             
            #im=Image.open(picture,"r")
            #im.tag.tags
            max=60
            if not self.options.silent: print "[",threadid,"] open: ",picture 
            for i in range(max):
                try:
                    image=misc.imread(picture)
                    #tif = TiffFile(picture)
                    #image = tif.asarray()
                    
                except KeyboardInterrupt:
                    return
                except IOError as e:
                    try:
                        print "cannot open ", picture, ", lets wait.", max-i ," s"
                        print e.message,  sys.exc_info()[0]
                        time.sleep(1)
                        continue
                    except KeyboardInterrupt:
                        return
                except:
                    print "############"
                    print   sys.exc_info()
                    continue
                if image.shape==tuple(self.cal.config["Imagesize"]):
                    break
                print "cannot open ", picture, ", lets wait.", max-i ," s"
                time.sleep(1)
                    
            else:
                print "image ", picture, " has wrong format"
                return
                
            if self.options.outdir!="":
                basename=self.options.outdir+os.sep+('_'.join(picture.replace('./','').split(os.sep))[:-3]).replace('/',"_")
                basename=basename.replace(':', '').replace('.','')+'.'
            else:
                reldir=os.path.join( 
                                      os.path.dirname(picture),
                                      self.options.relpath)
                if not os.path.isdir(reldir):
                    os.mkdir(reldir)
                basename=os.path.join( reldir,
                                      os.path.basename(picture)[:-3])
            
                
            if not self.options.resume or not os.path.isfile(basename+'chi'):
                data=self.cal.integratechi(image,basename+"chi")
                if threadid==0 and self.options.plotwindow:
                    # this is a hack it really schould be a proper GUI
                   
                    self.cal.plot(image,fig=self.fig)
                    plt.draw()
                   
                         
            if self.options.writesvg: 
                
                if not self.options.resume or not os.path.isfile(basename+'svg'):
                    self.cal.plot(image,basename+"svg",fig=self.fig)
            if self.options.writepng:
                 if not self.options.resume or not os.path.isfile(basename+'svg'):
                      misc.imsave(basename+"png",image)
               
            
            #self.picturequeue.task_done()
            with self.allp.get_lock():
                self.allp.value+=1
            if self.options.silent:
                
                if np.mod(self.allp.value,100)==0:
                    print "[",threadid,"] ",self.allp.value
            else:
                print "[",threadid,"] write: ",basename+"chi" 
            return basename ,data
    def start(self):  
        """
        Start threads and directory observer.
        """
       
 
            
         
        #start threads
        for threadid in range(1,self.options.threads):
            print "start proc [",threadid,"]"
           
            worker=Process(target=funcworker, args=(self,threadid))
            worker.daemon=True
            self.pool.append(worker)
            worker.start() 
            #self.processimage(picture,options)
        self.starttime=time.time() 
        if self.options.watch:
            eventhandler=addtoqueue(self.picturequeue)
            observer = Observer()
            observer.schedule(eventhandler, self.args[0], recursive=True)
            observer.start()
        #We let the master process do some work because its useful for matplotlib.
        if not self.dirwalker:
            self.dirwalker=Process()
            self.dirwalker.start()
        if self.options.servermode:
             
             context = zmq.Context()
             socket = context.socket(zmq.REQ)
             tokenlist=  self.conf['Server'].split(":")
             
             server=":".join([tokenlist[0],tokenlist[1],self.options.serverport])
             print server
             socket.connect (server)
             from Leash import addauthentication
        try:
            while ( self.options.servermode or 
                    (not self.picturequeue.empty()) 
                    or self.dirwalker.is_alive() 
                    or self.options.watch): 
                    try:
                        picture = self.picturequeue.get(timeout=1)
                    except KeyboardInterrupt :
                        break
                    except Empty:
                        continue
                    lastfile, data =self.procimage(picture,0)
                    if self.options.servermode:
                        request={"command":"putplotdata","argument":{"data":{
                                "result":"plot","data":{"filename":lastfile,"array":data.tolist(),"stat":{}}
                                  }}}
                        socket.send_multipart([json.dumps(addauthentication( request,conf))])
                        socket.recv()
                         
                    
                    if np.mod(self.allp.value,500)==0:
                        self.timreport()
        except  KeyboardInterrupt:            
            if self.options.watch:
                        observer.stop()
                        observer.join()   
            if self.options.servermode:
                 context.destroy()
        self.stop()
        self.timreport()
        return self.allp.value, time.time()-self.starttime
    
    def stop(self):
        print "\n\nWaiting for the processes to terminate."
        self.stopflag.value=1
        for worker in self.pool:
            worker.join(3)
            
    def timreport(self):
        
        tottime=time.time()-self.starttime
        if self.allp.value==0:
            print "We didn't do any pictures "
        else:
            print "\n\nelapsed time: ",tottime
            print "\nProcessed: ",self.allp.value," pic"
            print " time per pic: ", tottime/self.allp.value,"[s]"
            print " pic per second: ",self.allp.value/tottime,"[/s]"
        
    
