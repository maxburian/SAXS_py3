import SAXS,json
from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
conf=json.load(open('cal.json'))
img =SAXS.openmask(conf["Masks"][0]["MaskFile"])
img=img.astype(int)
plt.imshow(img,cmap='Greys')
plt.colorbar()
misc.imsave("mask.tif",img)