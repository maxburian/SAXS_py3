import json
from optparse import OptionParser
import os,re,sys
from jsonschema import validate,ValidationError
import time
import schematools
def txt2json(text,s):
            if not "Geometry" in s:
                s["Geometry"]={}
            print text
            for line in text.split('\n'):
                word=re.split('\s+', line)
                
                if re.search('Refined Beam centre.+pixels',line):
                    s["Geometry"]['BeamCenter']=[float(word[6]),float(word[5])]
                elif re.search('Refined sample to detector distance',line):
                    s["Geometry"]['DedectorDistanceMM']=float(word[7])
                elif re.search(' Refined tilt plane rotation angl',line):
                    if not "Tilt" in s["Geometry"] :s["Geometry"]["Tilt"]={}
                    s["Geometry"]['Tilt']['TiltRotDeg']=float(word[7])
                elif re.search(' Refined tilt angle ',line):
                    if not "Tilt" in s["Geometry"] :s["Geometry"]["Tilt"]={}
                    s["Geometry"]['Tilt']['TiltAngleDeg']=float(word[5])
                elif re.search('Refined wavelength =',line):
                    s['Wavelength']=float(word[4])
               
            return s
def jsontojson(fromjsontext,s):
    fromjson=json.loads(fromjsontext)
    schemalist=[{"path":os.path.dirname(__file__)+'/schema_1.json',
                  "pathtable":[
                       {"old":['Tilt'],                 "new":["Geometry","Tilt"]},
                       {"old":['Imagesize'],            "new":["Geometry","Imagesize"]},
                       {"old":['DedectorDistanceMM'],   "new":["Geometry","DedectorDistanceMM"]},
                       {"old":['BeamCenter'],           "new":["Geometry","BeamCenter"]},
                       {"old":['PolarizationCorrection'],"new":["PolarizationCorrection" ]},
                       {"old":['Wavelength'],           "new":["Wavelength"]},
                       {"old":['Title'],                "new":["Geometry","Title"]},
                       {"old":['PixelSizeMicroM'],      "new":["Geometry","PixelSizeMicroM"]},
                       {"old":['MaskFile'],             "new":["Masks",0,"MaskFile"]},
                       {"old":['PixelPerRadialElement'],"new":["Masks",0,"PixelPerRadialElement"]},
                       {"old":['Oversampling'],         "new":["Masks",0,"Oversampling"]}
                    ]
                  
            }]
    for schemadesc in schemalist:
          schema=(json.load(open(schemadesc["path"])))
         
          validate(fromjson,schema)
          for pathpair in schemadesc["pathtable"]:
              value=valuebypath(fromjson,pathpair["old"])
              setvaluebypath(s,pathpair["new"],value)
             
              
          
       
         
    print "unknown file format"
def valuebypath(jsonobj,path):
    subtree=jsonobj
    for key in path:
        if type(key) is str:
            if key in subtree:
                subtree=subtree[key]
            else:
                subtree=None
        elif type(key) is int:
            try:
                subtree=subtree[key]
            except:
                subtree=None
    return subtree
def setvaluebypath(jsonobj,path,value):
    
        if len(path)>1:
            if type(path[0]) is str and path[0] not in jsonobj:
                jsonobj[path[0]]={}
            setvaluebypath(jsonobj[path[0]],path[1:],value)
        else:
            if value:
                jsonobj[path[0]]=value
                print jsonobj
            elif path[0] in jsonobj:
                jsonobj.pop(path[0])
    
       
def convert():
    """
    This implements the functionality oft :ref:`converter`.
    It parses the commandline options and converts the
    Fit2d info file to the JSON data used by the SAXS.callibration class.
    """
    parser = OptionParser()
    usage = ("usage: %prog [options] calibration.txt ouput.saxsconf\n"
    +"or\n"
    +"%prog [options] cal.saxsconf ouput.saxsconf\n")
    parser = OptionParser(usage)
    parser.add_option("-t", "--template", dest="templatepath",
                      help="Path to calibration file which serves as template.", metavar="FILE",default="")
    (options, args) = parser.parse_args(args=None, values=None)
    schemapath=os.path.dirname(__file__)+'/schema.json'
    schema=(json.load(open(schemapath)))
    if len(args)!=2:
        parser.error("incorrect number of arguments")
        
    if os.path.isfile(args[1]):
        
        if options.templatepath!="":
            calfile=open(options.templatepath)
        else:
            calfile=open(args[1])
        caldict=json.load(calfile)
        
        print schemapath+",",__file__
      
        try:
            validate(caldict,schema)
        except ValidationError as e:
            print "Validation Error:"+e.message
            return
        s=caldict
        print "parsed atributes are added replaced in the target file"
 
    else:
        s=schematools.schematodefault(schema)
        
    with open(args[0])as infile:
        fromjson=None
        try:
            fromjson=json.load(infile)
        except Exception as e:
            print e
        if fromjson:
             jsontojson(json.dumps(fromjson),s)
        else:
             txt2json(open(args[0]).read(),s)
        with open(args[1],"w") as outfile:
             json.dump(s, outfile,  indent=4, separators=(',', ': '))
        print json.dumps(s, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    convert()

    