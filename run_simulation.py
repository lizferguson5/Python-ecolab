from scipy.io import loadmat
import ecolab
import matplotlib.pyplot as plt
import numpy as np


np.random.seed(1) # This is the same as rng(1) in MATLAB

print('Running ecolab in sync mode - results are equivalent to MATLAB original. Uses previous iteration values of agents')
(agents,env,history) = ecolab.ecolab(size=20, nr=200, nf=30, steps=100, mode='sync')
plt.plot(history[0,:])
plt.plot(history[1,:])
print('sync mode calculation complete')
plt.savefig('ecolab_sync.png')
plt.close()
print('Figure saved at ecolab_sync.png')
np.savetxt('ecolab_sync.csv',np.transpose(history),delimiter=',')
print('Data saved at ecolab_sync.csv\n')

np.random.seed(1) # This is the same as rng(1) in MATLAB
print('Running ecolab in async mode - uses real-time values of agents at all times')
(agents,env,history) = ecolab.ecolab(size=20, nr=200, nf=30, steps=100, mode='async')

plt.plot(history[0,:])
plt.plot(history[1,:])
print('async mode calculation complete')
plt.savefig('ecolab_async.png')
plt.close()
print('Figure saved at ecolab_async.png')
np.savetxt('ecolab_async.csv',history,delimiter=',')
print('Data saved at ecolab_async.csv')



