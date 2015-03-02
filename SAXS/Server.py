import sys
import zmq
from multiprocessing import Process
import time,json,datetime
import os
import atrdict
import calibration
from jsonschema import validate,ValidationError
import base64
import traceback
from optparse import OptionParser
import hashlib
import imagequeuelib
from Queue import Empty
internalplotsocked=345834

class AuthenticationError(Exception):
    """
    Custom error class
    """
    def __init__(self, value):
        self.message = value
        self.value=value
    def __str__(self):
        return repr(self.message)

def subscribeToFileChanges(imqueue,url,dir,serverdir):
    """
    Function to connect to file feeder service. Runs in Thread.
    """
    port = "5556"
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
            print serverdir
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
    def __init__(self,conf):
        self.files=None
       
        self.options, self.args=parsecommandline()
        if len(self.args)==0:
            self.args=["."]
        if   self.options.outdir!="" :
             parser.error('"'+self.options.outdir+'"'+" directory does not exist")
        if self.options.feederurl=="":
            self.feederurl=conf["Feeder"]
        self.serverconf=conf
        self.comandosocket=None
        
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
        dir=  os.path.join(self.args[0], os.sep.join(request["argument"]['directory']))
        try:
            files=os.listdir(os.path.join( dir))
        except OSError as e:
            return {"result":"OSError","data":{"Error":str(e)}}
        content=[]
        for item in files:
            if os.path.isdir(os.path.join(dir,item)):
                content.append({"isdir":True,"path":item})
          
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
        else:
            result={"result":"ErrorNotimplemented"}
       
         
        return result
    def start_image_queue(self,object,attachment):
        """
        prepare new image queue
        start processing threads
        """
        self.lasttime=time.time()
        self.lastcount=0
        self.attachments=[]
        for attachstr in attachment:
            self.attachments.append(json.loads(attachstr))
        self.calibration=object['argument']['calibration']
        print "abort old queue"
        if self.imagequeue:
             self.queue_abort()
        print "aborted old queue"
        try:
            if object['argument']['calibration'].get("Threads")>0:
                self.threads=object['argument']['calibration'].get("Threads")
            else:
                self.threads=self.options.threads
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
            for mnumber,mask in enumerate(object['argument']['calibration']["Masks"]):
                cals.append(calibration.calibration(
                                            object['argument']['calibration'],
                                            mask,
                                            self.attachments[mnumber]))
            self.imagequeue=imagequeuelib.imagequeue(cals,
                    o,[ dir],self.serverconf)
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
           
            result={"result":"queue initiated ","data":{"cal":object['argument']['calibration']}}
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
        except AttributeError as msg:
            result={"result":"ValueError","data":{"Error":"Start Queue first"}}
            return result
        return {"result":"queue restarted with all files","data":{"stat":self.stat()}}
    def plot(self):
        self.plotresult['data']["stat"]=self.stat()
        return  self.plotresult
    def updateplot(self,object):
        self.plotresult=object['argument']["data"]
        return {"result":"done","data":{}}
    def stat(self):
        if self.imagequeue:
          
            self.lasttime=time.time()
            newpic=self.imagequeue.allp.value-self.lastcount
            self.lastcount=self.imagequeue.allp.value
            return {"images processed":self.imagequeue.allp.value,
             "queue length":self.imagequeue.picturequeue.qsize(),
             "time":time.time(),
             "start time":self.queuestatrtime
         
             
             }
        else:
            return{}
def saxsdogserver(serverconf):
     
     S=Server(serverconf)
     
     S.start()
     
       
def startservers(serverconfs):
    Servers=[]
    for serverconf in serverconfs:
        Servers.append(Process(target=saxsdogserver,args=(serverconf,)))
        Servers[-1].start()
if __name__ == '__main__':
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