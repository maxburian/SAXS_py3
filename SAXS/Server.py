import sys
import zmq
from multiprocessing import Process
import time,json
import jsonschema
def subscribeToFileChanges():
    port = "5556"
 
    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    print "tcp://localhost:%s" % port
    socket.connect ("tcp://localhost:%s" % port)
    socket.setsockopt(zmq.SUBSCRIBE,"")
    while True:
       
        string = socket.recv()
        print "m:",string



class Server():
    def __init__(self):
        self.files=Process(target=subscribeToFileChanges,args=())
        self.files.start()
        context = zmq.Context()
        self.comandosocket = context.socket(zmq.REP)
        port="7777"
        self.comandosocket.bind("tcp://*:%s" % port)
        
    def start(self):
        while True:
            try:
                message=self.comandosocket.recv()
                self.comandosocket.send("reply:"+message)
            except Exception,msg:
                 error={"result":"Error","data":msg}
                 self.comandosocket.send(json.dumps(error))
            
if __name__ == '__main__':
     S=Server()
     S.start()
    