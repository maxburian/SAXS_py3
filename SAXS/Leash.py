import zmq
import random
import sys
import time
import os
import json
from optparse import OptionParser

def initcommand():
    parser = OptionParser()
    usage = "usage: %prog [options] calibration.txt ouput.json"
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port",
                      help="Port to offer file changes service", metavar="port",default="7777")
   
    (options, args) = parser.parse_args(args=None, values=None)
    
 
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    print "conecting:","tcp://localhost:%s" % options.port
    socket.connect ("tcp://localhost:%s" % options.port)
    socket.send("request")
    message=socket.recv()
    print message
                        

if __name__ == '__main__':
    initcommand()

    