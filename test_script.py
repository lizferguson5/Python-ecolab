from agents import rabbit,fox
from environment import environment
import ecolab
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(1)

#(rabbits,foxes,env) = ecolab.ecolab(size=10,nr=4,nf=4,steps=10)

(agents,env,history) = ecolab.ecolab_matlab(size=300,nr=100,nf=400,steps=100)
#plt.plot(history[0,:])
#plt.plot(history[1,:])
#plt.show()
#print(np.transpose(history))






