import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import SAXS,json
from scipy import misc
geo=json.load(open("calgeo.json"))
misc.imsave("emptymask.tif",np.zeros(geo["Geometry"]['Imagesize']))

Cal=SAXS.calibration(geo)
ring=Cal.I[100].todense().reshape((Cal.config["Geometry"]['Imagesize'][0],Cal.config["Geometry"]['Imagesize'][1]))
misc.imsave("ring.png",ring[110:350,250:550])
misc.imsave("ring.pdf",ring[110:350,250:550])
geo["Masks"][0]['Oversampling']=1
Calnov=SAXS.calibration(geo)
ringnov=Calnov.I[100].todense().reshape((Cal.config["Geometry"]['Imagesize'][0],Cal.config["Geometry"]['Imagesize'][1]))
misc.imsave("ringNoOv.png",ringnov[110:350,250:550])
misc.imsave("ringNoOv.pdf",ringnov[110:350,250:550])