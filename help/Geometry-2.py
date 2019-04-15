import matplotlib.pyplot as plt
import numpy as np
import SAXS,json
from scipy import misc
geo=json.load(open("calgeo.json","r"))
misc.imsave("emptymask.tif",np.zeros(geo["Geometry"]['Imagesize']))
Cal=SAXS.calibration(json.load(open("calgeo.json","r")))
rmax= 1003
x=np.arange(rmax)/100000.0 /3
y=(3*np.exp(-(x/6.0e-5)**2)
      +np.exp(-((x-0.5e-3)/1.0e-5)**2)
      +np.exp(-((x-1.0e-3)/1.0e-5)**2)
      +np.exp(-((x-1.5e-3)/1.0e-5)**2)
      +np.exp(-((x-2.0e-3)/1.0e-5)**2)
      +np.exp(-((x-2.50e-3)/1.0e-5)**2))


powder=Cal.ITransposed.dot((y*30000+1000)*Cal.Areas).reshape((Cal.config["Geometry"]['Imagesize'][0],Cal.config["Geometry"]['Imagesize'][1]))*10000
misc.imsave("powder.tif", powder)
plt.imshow(powder)
plt.title(r"Simulated Powder Diffraction")