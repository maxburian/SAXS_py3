import random
import json
import os,sys
from jsonschema import validate,ValidationError
def createsaxdogconf():
    server=raw_input( "Please enter the Saxsdog Server URL (tcp://hostname:port):\n")
    feeder=raw_input("Please enter the file events feeder service URL (tcp://hostname:port):\n")
    secret='%030x' % random.randrange(16**30)
    if server=="":server="tcp://localhost:9723"
    if feeder=="":feeder="tcp://localhost:9823"
    content={"Server":server,"Feeder":feeder,"Secret":secret}
    try:
        validate(content,json.load(open(os.path.dirname(__file__)+os.sep+'NetworkSchema.json')))
    except ValidationError as e:
        print "Error in config file: ",e.message
        sys.exit()
    json.dump(content,open(os.path.expanduser("~"+os.sep+".saxdognetwork"),"w"))
    print os.path.expanduser("~"+os.sep+".saxdognetwork")," created. \n\n Copy it to the other machines who take part in your network"

if __name__ == '__main__':
    createsaxdogconf()