import threading 
import  multiprocessing
import os
def Process(target=None,args=()):
    if os.sys.platform=="win32":
        return threading.Thread(target=target, args=args)
    else:
        return multiprocessing.Process(target=target, args=args)