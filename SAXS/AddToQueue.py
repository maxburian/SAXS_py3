from watchdog.events import FileSystemEventHandler
import os
class addtoqueue(FileSystemEventHandler):
    '''Sub-class of watchdog event handler, used for detecting file system events.'''
    
    def __init__(self, queue,config=None, log=None):
        self.log = log
        self.config = config
        self.queue=queue
        self.last=""
    
    def on_created(self, event):
        file = os.path.basename(event.src_path)
        
        if file.endswith('tif'):
            if file != self.last:
                self.queue.put(event.src_path)
                self.last=file
        
    def on_modified(self, event):
        file = os.path.basename(event.src_path)
        
        if file.endswith('tif'):
            if file != self.last:
                self.queue.put(event.src_path)
                self.last=file
      