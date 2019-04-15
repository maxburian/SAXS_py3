import SAXS, json
import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
calfile=json.load(open('calpol.json'))
calfile["Masks"][0]['Oversampling']=2
calfile["Geometry"]['BeamCenter']=[293,600]
Cal=SAXS.calibration(calfile)

s=Cal.plot(misc.imread('data/buf1_00000.tif'),outputfile="bad.svg")
plt.title(r"Wrong Beam Center")