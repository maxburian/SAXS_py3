import random
import json
import os, sys
from optparse import OptionParser
from subprocess import call
from jsonschema import validate, ValidationError
def createsaxdogconf():
    """
    utility to simplify creating config files for SAXSdog  Network
    """
    parser = OptionParser()
    usage = "usage: %prog [options] "
    parser = OptionParser(usage)
    parser.add_option("-n", "--new", dest="new",  action="store_true", default=False,
                      help="replace old config and generate new secret")
    (options, args) = parser.parse_args(args=None, values=None)
    
    confpath=os.path.expanduser("~"+os.sep+".saxsdognetwork")
    if os.path.isfile(confpath) and not options.new:
        content=json.load(open(confpath))
    else:
        server="tcp://localhost:9723"
        feeder="tcp://localhost:9823"
        secret='%030x' % random.randrange(16**30)
        content=[{"Server":server,"Feeder":feeder,"Secret":secret,"Name":"Queue1"}]
        json.dump(content, open(confpath, "w"), indent=4, separators=(',', ': '))
    
    if  os.name == "nt":
        call(["notepad", confpath ])
    elif os.name == "posix": 
        call(["vi", confpath ])
    content=json.load(open(confpath))
    try:
        validate(content, json.load(open(os.path.dirname(__file__)+os.sep+'NetworkSchema.json')))
    except ValidationError as e:
        print("Error in config file: ", e.message)
        sys.exit()
    json.dump(content, open(confpath, "w"), indent=4, separators=(',', ': '))
    print(confpath, " created. \n\n Copy it to the other machines who take part in your network")

if __name__ == '__main__':
    createsaxdogconf()