import zmq
import random
import sys
import time
import os
import json
from optparse import OptionParser

def startfeeder():
    """
    Simulator for new file anounciation service. For development and testing.
    """
    parser = OptionParser()
    usage = "usage: %prog [options]  "
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port",
                      help="Port to offer file changes service", metavar="port", default="")
    parser.add_option("-d", "--dir", dest="dir",
                      help="Directory to monitor", metavar="dir", default=".")
    parser.add_option("-s", "--sdir", dest="sdir",
                      help="server dir, (prefix to filepaths)", metavar="dir", default=".")
    (options, args) = parser.parse_args(args=None, values=None)
    
    
    
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    if options.port=="":
        conf=json.load(open(os.path.expanduser("~"+os.sep+".saxsdognetwork"))) 
        port=conf['Feeder'].split(':')[-1]
    else:
        port=options.port
    print("conecting:", "tcp://*:%s" % port)
    socket.bind("tcp://*:%s" % port)
    
    fileslist=[]
    if len(args)>0 and options.dir==".":
        dirtosearch =args[0]
    else:
        dirtosearch =options.dir
    for path, subdirs, files in os.walk(dirtosearch):
                for name in files:
                    if name.endswith('tif'):
                        fileslist.append( os.path.join(path, name))
    messageobj={"command":"new file","argument":""}
    while True:
       for file in fileslist:
            print(file)
            messageobj['argument']=file
            message=json.dumps(messageobj)
            socket.send(message)
            time.sleep(7)
                        

if __name__ == '__main__':
    startfeeder()

    