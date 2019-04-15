import SAXS, json
import matplotlib.pyplot as plt
import numpy as np
calfile=json.load(open('calpol.json'))
calfile["Masks"][0]['Oversampling']=2
Calpol=SAXS.calibration(calfile)
r=Calpol.integrate(np.ones(Calpol.corr.shape))
nonzero=r[1]>0
plt.plot(r[0][nonzero],r[1][nonzero])
plt.title(r"Integration of Picture With Constant Value 1")