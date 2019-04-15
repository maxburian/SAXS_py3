import matplotlib.pyplot as plt
import numpy as np
data=np.loadtxt('data/fit2d' ,skiprows=4 )
plt.plot(data[:,0],data[:,1],label="fit2d")
data=np.loadtxt('data/saxsdog' ,skiprows=4 )
plt.plot(data[:,0],data[:,1],label="saxsdog")
plt.ylabel('Intensity [counts/pixel]')
plt.xlabel('q [1/nm]')
plt.yscale('log')
plt.title("Compare Fit2d and SAXS Package")