import sys 
sys.path.append("../../jsonSchemaToRsT")
sys.path.append("../")
from jsonSchemaToRsT import *
import json
import collections
 
 
transform=jsonschematorst( '../SAXS/schema.json') 

RST= transform.toRsT()
#print RST 
#print RST
rstfile=open("SAXSSchema.rst",'w')
rstfile.write(RST)
rstfile.close

transform=jsonschematorst( '../SAXS/LeashRequestSchema.json') 

RST= transform.toRsT()
#print RST 
#print RST
rstfile=open("SAXSLeashRequest.rst",'w')
rstfile.write(RST)
rstfile.close

transform=jsonschematorst( '../SAXS/LeashResultSchema.json') 

RST= transform.toRsT()
#print RST 
#print RST
rstfile=open("SAXSLeashResult.rst",'w')
rstfile.write(RST)
rstfile.close
