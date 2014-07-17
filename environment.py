import numpy as np

class environment:
    def __init__(self,size):
        self.bm_size= size
        
        #distribute food - 50 per square
        self.food= np.floor(50*np.ones((size,size)))

        #generate patch where there is no food
        self.food[np.round(0.6*size)-1:np.round(0.8*size),np.round(0.6*size)-1:np.round(0.8*size)] = 0