import sys
import zmq
from multiprocessing import Process
import time,json,datetime
import os
import atrdict
import calibration
from jsonschema import validate,ValidationError
import GISAXSSlices
import datamerge
from optparse import OptionParser
import hashlib
import imagequeuelib

internalplotsocked=345834
import Leash
class DirectoryCollisionException(Exception):
    pass

class AuthenticationError(Exception):
    """
    Custom error class
    """
    def __init__(self, value):
        self.message = value
        self.value=value
    def __str__(self):
        return repr(self.message)
class history():
    def __init__(self):
        self.hist=[]
        self.filelist={}
    def update(self,queue):
        hist=[]
        now=time.time()
        for timest in self.hist:
            if now-timest<100:
                hist.append(timest)
        while True:
            try:
                item=queue.get(False)
            except Exception as e : 
              
                break
            if item:
                hist.append(item["Time"])
                self.filelist[item["BaseName"]]=item["FileList"]
            
        self.hist=hist
def subscribeToFileChanges(imqueue,url,dir,serverdir):
    """
    Function to connect to file feeder service. Runs in Thread.
    """
  
    queue=imqueue.picturequeue
    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    print "Feeder at: ",url
    print "serverdir " + serverdir
    print "selectdir " + dir
    socket.connect ( url)
    socket.setsockopt(zmq.SUBSCRIBE,"")
    try:
        while imqueue.stopflag.value==0: 
           
            string = socket.recv()
            obj=json.loads(string)
            file=os.path.abspath(os.path.normpath(os.path.join(serverdir, obj['argument'])))
          
            print file
            if file.startswith( os.path.abspath(os.path.normpath(dir))):
                if file.endswith('.tif'):
                    queue.put( file)
    except KeyboardInterrupt:
        context.destroy()
def parsecommandline():
    
        parser = OptionParser()
        usage = "usage: %prog [options] basedir"
        parser = OptionParser(usage)
        parser.add_option("-p", "--port", dest="port",
                      help="Port to offer command service. Default is 7777.", metavar="port",default="") 
        
        parser.add_option("-t", "--threads",type="int", dest="threads",
                      help="Number of concurrent processes.",default=1)
        parser.add_option('-f','--feeder',dest="feederurl",metavar="tcp://hostname:port",default="",
                          help="Specify the URL of the new file event service (Saxsdog Feeder)"
                          )
        
        parser.add_option("-w", "--watch", dest="watchdir", default=False,action="store_true",
                      help="Watch directory for changes, using file system events recursively for all sub directories.")
      
        parser.add_option("-R", "--relpath", dest="relpath", default="../work",
                      help="Specify output directory as relative path to image file. Default: '../work'")
    
        parser.add_option("-o", "--out", dest="outdir", default="",
                      help="Specify output directory")
        
        parser.add_option("-d", "--daemon", dest="daemon", default=False,action="store_true",
                      help="Start server  as daemon")
   
        return  parser.parse_args(args=None, values=None)

class Server():
    """
    class to manage a saxsdog server
    """
    def __init__(self,conf,serverid):
        self.files=None
        self.serverid=serverid
        self.options, self.args=parsecommandline()
        if len(self.args)==0:
            self.args=["."]
        if   self.options.outdir!="" :
              print '"'+self.options.outdir+'"'+" directory does not exist"
              sys.exit()
        if self.options.feederurl=="":
            self.feederurl=conf["Feeder"]
        self.serverconf=conf
        self.comandosocket=None
        self.serverdir=self.args[0]
        self.commandschema=json.load(open(os.path.abspath(os.path.dirname(__file__))+'/LeashRequestSchema.json'))
        self.imagequeue=None
        self.feederproc=None
        self.threads=self.options.threads
        self.plotresult={"result":"Empty","data":{  "stat":{"images processed": 0,
                     "queue length":0,
                     "time":time.time(),
                     
                     }}}
           
    def start(self):
        """
        start server loop
        """
        if self.options.port=="":
            self.serverport=self.serverconf['Server'].split(':')[-1]
        else:
            self.serverport=self.options.port
        self.secret=self.serverconf['Secret']
        context = zmq.Context()
        self.comandosocket = context.socket(zmq.REP)
        print "server listenes at tcp://*:%s" % self.serverport
        self.comandosocket.bind("tcp://*:%s" % self.serverport)
       
        while True:
            try:
                message=self.comandosocket.recv_multipart()
                 
                object=json.loads(message[0])
                validate(object,self.commandschema)
                self.authenticate(object)
                attachment=message[1:]
                result=self.commandhandler(object,attachment)
            except ValidationError as e:
                result={"result":"ValidationError in request","data":e.message}
            except ValueError as e:
                result={"result":"ValueError in request","data":{"Error":e.message}}
            except  AuthenticationError as e:
                 result={"result":"AuthenticationError in request","data":{"Error":e.message}}
            except KeyboardInterrupt:
                context.destroy()
                self.queue_abort()
            except Exception as e:
                result={"result":"ServerError","data":{"Error":e.message}}
                print e
            try:
                self.comandosocket.send(json.dumps(result))
            except Exception as e:
                result={"result":"ServerError","data":{"Error":e.message}}
                self.comandosocket.send(json.dumps(result))
           
            
    def authenticate(self,data):
        """
        check signature of request
        """
        sign=data['sign']
        data["sign"]=""
        m=hashlib.sha512()
        now=time.time() 
         
        m.update(json.dumps(data, sort_keys=True))
        m.update(self.secret)
        if not abs(data["time"]-now)<900:
            raise AuthenticationError("Untimely request.")
        if not sign==m.hexdigest():
            raise AuthenticationError("Wrong signature.")
        
                
            
    def listdir(self,request):
        print self.args[0]
        dir=  os.path.join(self.args[0], os.sep.join(request["argument"]['directory']))
        try:
            files=os.listdir(os.path.join( dir))
        except OSError as e:
            return {"result":"OSError","data":{"Error":str(e)}}
        content=[]
        for item in files:
            if os.path.isdir(os.path.join(dir,item)):
                content.append({"isdir":True,"path":item})
            else:
                content.append({"isdir":False,"path":item})
        return {"result":"listdir","data":{"dircontent":content,"directory":dir.split(os.sep)}}
    def commandhandler(self,object,attachment):
        """
        
        """
        command=object['command']
        print "got: "+ command 
        if command=='new':
            result= self.start_image_queue(object,attachment)
            print str(datetime.datetime.now())+": new queue for:"
            if object['argument']['calibration'].get("Directory"):
                print "    '"+os.sep.join(object['argument']['calibration'].get("Directory"))+"'"
        elif command=='abort':
             result=self.queue_abort()
        elif command=='close':
             result=self.queue_close()
        elif command=="readdir":
             result=self.readdir(object)
        elif command=="listdir":
             result=self.listdir(object)
        elif command=="putplotdata":
             result=self.updateplot(object)
        elif command=="plot":
             if self.imagequeue:
                result=self.plot()
             else:
                result={"result":"no queue","data":{}}
        elif command=="stat":
             result={"result":"stat","data":{"stat":self.stat()}}
        elif command=="get":
            if self.imagequeue:
                 result={"result":"cal","data":{
                                                "cal":self.calibration,
                                               
                                                "attachments":self.attachments
                                                }}
            else:
                result={"result":"no queue","data":{}}
        elif command=="fileslist":
            result=self.getresultfileslists()
        elif command=="mergedata":
            result=self.mergedatacommand( object['argument']["mergeconf"])
        else:
            result={"result":"ErrorNotimplemented","data":{"Error":command+" not implemented"}}
       
         
        return result
    def start_image_queue(self,object,attachment):
        """
        prepare new image queue
        start processing threads
        """
        self.lasttime=time.time()
        self.lastcount=0
        self.history=history()
        self.attachments=[]
        
        
        try:
            self._checkdirectorycollision(object['argument']['calibration']['Directory'])
            for attachstr in attachment:
                self.attachments.append(json.loads(attachstr))
            self.calibration=object['argument']['calibration']
            if object['argument']['calibration'].get("Threads")>0:
                self.threads=object['argument']['calibration'].get("Threads")
            else:
                self.threads=self.options.threads
            
            print "abort old queue"
            if self.imagequeue:
                 self.queue_abort()
            print "aborted old queue"
            
            o=atrdict.AttrDict({"plotwindow":False,"threads":self.threads,
                    		"watch":self.options.watchdir,
                            "watchdir":os.sep.join(object['argument']['calibration'].get("Directory")),
                            "servermode":True,
                            "silent":True,"plotwindow":False,
                            "walkdirinthreads":True,
                    		"outdir":self.options.outdir,
                            "relpath":self.options.relpath,
                    		 "writesvg":False,
                             "writepng":False,"resume":False,
                             "serverport":self.serverport
                             })
            cals=[]
            
            dir=os.path.normpath(
                os.path.join(
                             self.args[0],
                             os.sep.join(object['argument']['calibration'].get('Directory')
                            )))
            if "Masks" in object['argument']['calibration']:
                for mnumber,mask in enumerate(object['argument']['calibration']["Masks"]):
                    cals.append(calibration.calibration(
                                                object['argument']['calibration'],
                                                mask,
                                                self.attachments[mnumber]))
            if "Slices" in   object['argument']['calibration']:
                for slice in object['argument']['calibration']["Slices"]:
                    cals.append(GISAXSSlices.slice( object['argument']['calibration'],slice,self.attachments))
            self.imagequeue=imagequeuelib.imagequeue(cals,
                    o,dir,self.serverconf)
            print "startimgq"
            self.imagequeueprocess=Process(target=self.imagequeue.start)
            self.imagequeueprocess.start()
            print "listening to feeder"
            serverdir=self.args[0]
            self.feederproc=Process(target=subscribeToFileChanges,args=
                                    (self.imagequeue,
                                     self.feederurl,
                                    dir,
                                    serverdir
                                    )
                                    )
            print "directory to watch "+dir
        
            self.feederproc.start()
            
            self.queuestatrtime=time.time()
            self.plotresult={"result":"Empty","data":{"stat":self.stat()}}
           
            result={"result":"new queue","data":{"cal":object['argument']['calibration']}}
        except IOError as e: 
            result={"result":"IOError","data":{"Error": str(e).replace("\n"," ")}}
        except ValueError as e:
            result={"result":"ValueError","data":{"Error": str(e)}}
        except Exception as e:
            result={"result":"Error","data":{"Error": str(e)}}
            print e
        return result
    def queue_abort(self):
        if self.imagequeue:
            self.imagequeue.stop()
            self.imagequeueprocess.terminate()
            self.imagequeueprocess.join(1)
        self.queue_close()
        self.imagequeue=None
        return {"result":"queue aborted","data":{"stat":self.stat()}}
    def queue_close(self):
        if self.feederproc:
            self.feederproc.terminate()
            self.feederproc.join(0)
        return {"result":"queue closed","data":{"stat":self.stat()}}
    def readdir(self,object):
        
        
        try:
            self.imagequeue.fillqueuewithexistingfiles()
            pass
        except AttributeError  :
            result={"result":"ValueError","data":{"Error":"Start Queue first"}}
            return result
        return {"result":"queue restarted with all files","data":{"stat":self.stat()}}
    def plot(self):
        self.plotresult['data']["stat"]=self.stat()
        self.plotresult['data']["history"]=self.history.hist
        return  self.plotresult
    def updateplot(self,object):
        self.plotresult=object['argument']["data"]
        return {"result":"done","data":{}}
    def stat(self):
        if self.imagequeue:
            self.lasttime=time.time()
          
            self.lastcount=self.imagequeue.allp.value
            self.history.update(self.imagequeue.histqueue)
            return {"images processed":self.imagequeue.allp.value,
             "queue length":self.imagequeue.picturequeue.qsize(),
             "time":time.time(),
             "start time":self.queuestatrtime
             
             }
        else:
            return{}
    def getresultfileslists(self):
        filelists={}
        for basename in sorted(self.history.filelist.keys()):
            fileset= self.history.filelist[basename]
            for kind in fileset.keys():
                if kind in  filelists :
                    filelists[kind].append(fileset[kind])
                else:
                    filelists[kind]=  [fileset[kind]]
        return {"result":"resultfileslists","data":{"fileslist":filelists}}
    def mergedatacommand(self,conf):
        directory=os.path.normpath(
                    os.path.join(self.serverdir, os.sep.join(self.calibration["Directory"])))
        conf["OutputFileBaseName"]= directory.split(os.sep)[-1]+conf["OutputFileBaseName"]
        print "Dir: "+ directory
        for table in conf["LogDataTables"]:
            for file in table["Files"]:
                file["Path"].insert(0,self.serverdir)
        mergedTable,filelists,plotdata=datamerge.mergedata(conf,directory)
        resultdir=os.path.join(directory,"../result")
        if not  os.path.isdir(resultdir):
            os.mkdir(resultdir)
        datamerge.writeTable(conf,mergedTable,directory=resultdir)
        datamerge.writeFileLists(conf ,filelists,directory=resultdir,serverdir=self.serverdir)
        return {"result":"mergedata","data":{"syncplot":plotdata,"fileslist":filelists}}
    def _checkdirectorycollision(self,pathlist):
         serverconfs=json.load(open(os.path.expanduser("~"+os.sep+".saxsdognetwork")))
         mydir=os.path.normpath(os.sep.join(pathlist))
         
         for i,conf in enumerate(serverconfs):
            if i!=self.serverid:
                argu=["get"]
                opt=atrdict.AttrDict({"serverno":i,"server":conf["Server"]})
                result=json.loads(Leash.initcommand(opt,argu,conf))
                if result['result']=="cal":
                    otherpath=os.path.normpath(os.sep.join(result["data"]["cal"]['Directory']))
                    
                
                    if ((otherpath.startswith(mydir) or mydir.startswith(otherpath))
                        or (otherpath=="." or mydir==".")):
                        raise DirectoryCollisionException("Directory collides with: "+otherpath)
            
def saxsdogserver(serverconf,serverid):
     
     S=Server(serverconf,serverid)
     
     S.start()
     
       
def startservers(serverconfs):
    Servers=[]
    for serverid,serverconf in enumerate(serverconfs):
        Servers.append(Process(target=saxsdogserver,args=(serverconf,serverid)))
        Servers[-1].start()

def launcher():
     serverconfs=json.load(open(os.path.expanduser("~"+os.sep+".saxsdognetwork")))
     validate(serverconfs,json.load(open(os.path.dirname(__file__)+os.sep+'NetworkSchema.json')))
     options,args=parsecommandline()
     if not options.daemon:
         startservers(serverconfs)
     else:
        try:
            import daemon
        except Exception:
            print "'Daemon mode' requires the 'python-daemon' module and works only on Unix."
            sys.exit()
        logfile=open("saxsdoglog","w")
        with daemon.DaemonContext(stderr=logfile,stdout=logfile,working_directory="./"):
            startservers(serverconfs)
if __name__ == '__main__':
    launcher()
    