import zmq
import random
import sys
import time
import os
import json
from optparse import OptionParser
import base64
import SAXS
import numpy as np
import matplotlib.pyplot as plt
from jsonschema import validate,ValidationError
def sendclose(options,arg,socket):
    request={"command":"close","argument":{}}
    socket.send_multipart([json.dumps(request)])
    message=socket.recv()
    print message
def sendabort(options,arg,socket):
    request={"command":"abort","argument":{}}
    socket.send_multipart([json.dumps(request)])
    message=socket.recv()
    print message
def sendplot(options,arg,socket):
    
    
    plt.ion()
    while True:
        request={"command":"plot","argument":{}}
        socket.send_multipart([json.dumps(request)])
        message=socket.recv()
        
        object=json.loads(message)
        print object['data']['filename']
        data=np.array(object['data']['array']).transpose()
      
        
        skip=options.skip
        clip=options.clip
        clipat=0
        plt.plot(data[skip:-clip,0],data[skip:-clip,1])
        plt.fill_between( data[skip:-clip,0] ,
                   np.clip(data[skip:-clip,1]-data[skip:-clip,2],clipat,1e300),
                   np.clip(data[skip:-clip,1]+data[skip:-clip,2],clipat,1e300),
                   facecolor='blue' ,alpha=0.2,linewidth=0,label="Count Error")
        plt.title(object['data']['filename'])
        plt.ylabel('Intensity [counts/pixel]')
        plt.xlabel('q [1/nm]')
        plt.yscale(options.yax)
        plt.xscale(options.xax)
        plt.draw()
        plt.clf()
            
    
def sendreaddir(options,arg,socket):
    request={"command":"readdir","argument":{}}
     
    socket.send_multipart([json.dumps(request)])
    message=socket.recv()
    print message
def sendnew(options,arg,socket):
    request={ 
             "command":"new",
             "argument":{
                         "directory":"directory of data to take into account",
                         "calibration":{},
                         "maskbin":""
                         }
             }
    if len(arg)==4:
        try:
            cal=json.load(open(arg[1]))
            calschema=json.load(open(os.path.dirname(__file__)+'/schema.json'))
            validate(cal,calschema)
            request['argument']['calibration']=cal
            request['argument']['maskbin']="#attachment"
            request['argument']['directory']=arg[3]
        except (ValueError) as e:
            print e
            print "The calibration File, "+arg[1]+",is not Valid"
            sys.exit()
        except ValidationError as e:
           
            print e.message
            print "The calibration File, "+arg[1]+",is not Valid"
            sys.exit()
        
    else:
        print "Error"
        print "new command:"
        print "usage: leash new clibrationfile.json maskfile.msk directory"
    socket.send_multipart((json.dumps(request),
                           json.dumps({"filename":arg[2],"data":base64.b64encode(open(arg[2]).read())})
                           )
                          )
    message=socket.recv()
    print message
    
def initcommand(options, arg):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    print "conecting:","tcp://localhost:%s" % options.port
    socket.connect ("tcp://localhost:%s" % options.port)
    if arg[0]=="close":
        sendclose(options,arg,socket)
    elif arg[0]=="new":
        sendnew(options,arg,socket)
    elif arg[0]=="abort":
        sendabort(options,arg,socket)
    elif arg[0]=="plot":
        sendplot(options,arg,socket)
    elif arg[0]=="readdir":
        sendreaddir(options,arg,socket)
    else:
        raise ArgumentError(arg[0])
    
    
    
                        
def parsecommandline():
    
    parser = OptionParser()
    usage = "usage: %prog [options]  command [arguments]"
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port",
                      help="Port to offer image queue service", metavar="port",default="7777") 
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
    
if __name__ == '__main__':
    (options,arg)=parsecommandline()
    initcommand(options,arg)
    
    