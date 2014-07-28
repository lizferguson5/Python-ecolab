from scipy.io import loadmat
import ecolab
import matplotlib.pyplot as plt
import numpy as np


np.random.seed(1)


matlab_results = loadmat('fox_rabbit_20_60_5.mat')
matlab_data = matlab_results['the_data']

(agents,env,history) = ecolab.ecolab(size=60,nr=240,nf=5,steps=1000,mode='async')

plt.plot(history[0,:])
plt.plot(history[1,:])
plt.show()
print(np.transpose(history))






