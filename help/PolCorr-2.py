import SAXS, json
import matplotlib.pyplot as plt
import numpy as np
calfile=json.load(open('calpol.json'))
calfile["Masks"][0]['Oversampling']=2
Calpol=SAXS.calibration(calfile)
r=Calpol.integrate(1/Calpol.corr)
nonzero=r[1]>0
plt.title(r"Integration of Polarizationcorrection$^{-1}$")
plt.plot(r[0][nonzero],r[1][nonzero])