import zmq
import random
import sys
import time
import os
import json
from optparse import OptionParser

def startfeeder():
    parser = OptionParser()
    usage = "usage: %prog [options]  "
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port",
                      help="Port to offer file changes service", metavar="port",default="")
    parser.add_option("-d", "--dir", dest="dir",
                      help="Directory to monitor", metavar="dir",default=".")
    (options, args) = parser.parse_args(args=None, values=None)
    
 
    
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    if options.port=="":
        conf=json.load(open(os.path.expanduser("~"+os.sep+".saxdognetwork"))) 
        port=conf['Feeder'].split(':')[-1]
    else:
        port=options.port
    print "conecting:","tcp://*:%s" % port
    socket.bind("tcp://*:%s" % port)
    
    fileslist=[]
    for path, subdirs, files in os.walk(options.dir):
                for name in files:
                    if name.endswith('tif'):
                        fileslist.append( os.path.join(path, name))
    messageobj={"command":"new file","argument":""}
    while True:
       for file in fileslist:
            messageobj['argument']=file
            message=json.dumps(messageobj)
            print "."
            socket.send(message)
            time.sleep(.03)
                        

if __name__ == '__main__':
    startfeeder()

    