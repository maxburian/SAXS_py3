import SAXS,json
from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
conf=json.load(open('cal.json'))
img =SAXS.openmask(conf["Masks"][0]["MaskFile"])
img=img.astype(float)
cal=SAXS.calibration(conf)
r=cal.integrate(img)
nonzero=(r[1]!=0)
plt.plot(r[0][nonzero],r[1][nonzero])