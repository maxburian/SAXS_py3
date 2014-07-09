import zmq
import random
import sys
import time
import os
import json
from optparse import OptionParser
import base64

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import SAXS
from jsonschema import validate,ValidationError
def validateResponse(message):
    
    try:    
        resp=json.loads(message)
        respschema=json.load((open(os.path.dirname(__file__)+os.sep+'LeashResultSchema.json')) )
        validate(resp,respschema)
    except ValidationError as e:
        print "\nError in response data format:\n"
        print e.message
    
def sendclose(options,arg,socket):
    request={"command":"close","argument":{}}
    socket.send_multipart([json.dumps(request)])
    message=socket.recv()
    print message
    
    validateResponse(message)
   
def sendabort(options,arg,socket):
    request={"command":"abort","argument":{}}
    socket.send_multipart([json.dumps(request)])
    message=socket.recv()
    print message
    validateResponse(message)
    
def sendplot(options,arg,socket):
    
    
    plt.ion()
    while True:
        request={"command":"plot","argument":{}}
        socket.send_multipart([json.dumps(request)])
        message=socket.recv()
        validateResponse(message)
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
    validateResponse(message)
   
def sendstat(socket):
    request={"command":"stat","argument":{}}
    socket.send_multipart([json.dumps(request)])
    message=socket.recv()
    print message
    validateResponse(message)
   
    
def sendnew(options,arg,socket):
    request={ 
             "command":"new",
             "argument":{
                         "directory":"directory of data to take into account",
                         "calibration":{},
                          
                         }
             }
    if len(arg)==4:
        try:
            cal=json.load(open(arg[1]))
            calschema=json.load(open(os.path.dirname(__file__)+'/schema.json'))
            validate(cal,calschema)
            request['argument']['calibration']=cal
           
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
        sys.exit()
    socket.send_multipart((json.dumps(request),
                           json.dumps({"filename":arg[2],"data":base64.b64encode(open(arg[2],"rb").read())})
                           )
                          )
    message=socket.recv()
    print message
    
    validateResponse(message)
   
def initcommand(options, arg):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    print "conecting:",options.server
    socket.connect (options.server)
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
    elif arg[0]=="stat":
        sendstat(socket)
    else:
        raise ValueError(arg[0])
    
    
    
                        
def parsecommandline():
    
    parser = OptionParser()
    usage = ("usage: %prog "+
             '|'.join(
                      json.load(open(os.path.dirname(__file__)+'/LeashRequestSchema.json')
                        )["properties"]["command"]['enum']
                      ) +" [options] [arguments]"
       )
    parser = OptionParser(usage)
    parser.add_option("-S", "--server", dest="server",
                      help='URL of "Saxsdog Server"', metavar="tcp://HOSTNAME:PORT",default="tcp://localhost:7777") 
    parser.add_option("-s", "--skip", dest="skip",
                          help="plot: Skip first N points."
                          , metavar="N",default=0 ,type="int")   
    parser.add_option("-k", "--clip", dest="clip",
                      help="plot: Clip last N points."
                      , metavar="N",default=1 ,type="int")
    parser.add_option("-x",'--xaxsistype',dest='xax',metavar='TYPE',default='linear',
                       help="plot: Select type of X axis scale, might be [linear|log|symlog]")
    parser.add_option("-y",'--yaxsistype',dest='yax',metavar='TYPE',default='linear',
                       help="plot: Select type of Y axis scale, might be [linear|log|symlog]")
        
    
    
    (options, args) = parser.parse_args(args=None, values=None)
    if len(args)<1:
        parser.error("incorrect number of arguments")
        
    return  (options, args)
def saxsleash():
    (options,arg)=parsecommandline()
    initcommand(options,arg)
    
if __name__ == '__main__':
    saxsleash()
    