import SAXS, json
import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
calfile=json.load(open('calpol.json'))
calfile["Masks"][0]['Oversampling']=2
Calpol=SAXS.calibration(calfile)

s=Calpol.plot(misc.imread('data/buf1_00000.tif'),outputfile="good.svg")
plt.title(r"Standard Deviation")