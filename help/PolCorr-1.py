import SAXS, json
import matplotlib.pyplot as plt
import numpy as np

Calpol=SAXS.calibration('calpol.json')
plt.imshow(Calpol.corr)
plt.title(r"Polarization Correction")
plt.colorbar()