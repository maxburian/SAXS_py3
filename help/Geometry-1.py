import matplotlib.pyplot as plt
import numpy as np
rmax= 1003
x=np.arange(rmax)/100000.0 /3
y=(3*np.exp(-(x/6.0e-5)**2)
        +np.exp(-((x-0.5e-3)/1.0e-5)**2)
        +np.exp(-((x-1.0e-3)/1.0e-5)**2)
        +np.exp(-((x-1.5e-3)/1.0e-5)**2)
        +np.exp(-((x-2.0e-3)/1.0e-5)**2)
        +np.exp(-((x-2.50e-3)/1.0e-5)**2))
plt.plot(y)
plt.title(r"Simulated Powder Diffraction")
plt.ylabel("Intensity")
plt.xlabel("$n^{th}$ r")