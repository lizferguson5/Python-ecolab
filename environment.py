import numpy as np
from agents import rabbit,fox
from numpy.random import rand

class environment:
    def __init__(self,size):
        self.bm_size= size
        
        #distribute food - 50 per square
        self.food= np.floor(50*np.ones((size,size)))

        #generate patch where there is no food
        self.food[np.round(0.6*size)-1:np.round(0.8*size),np.round(0.6*size)-1:np.round(0.8*size)] = 0

    def create_agents(self,nr, nf):
        """
        create_agents(nr, nf)

        Creates a list of agents within the environment

        Input:

        nr - Integer: Number of rabbits
        nf - Integer: Number of foxes

        output:
        agent_list - Lists of generated agents


        """
        # We create the transpose here in order to generate matrices that are identical to MATLAB's
        # generate random initial positions for rabbits and foxes

        rloc = np.transpose((self.bm_size-1)*rand(2, nr))+1
        floc = np.transpose((self.bm_size-1)*rand(2, nf))+1

        self.rabbits = []
        self.foxes = []

        for r in range(nr):
            pos = rloc[r, :]
            age = np.ceil(rand()*10)
            food = np.ceil(rand()*20)+20
            lbreed = np.round(rand()*rabbit.brdfq)
            self.rabbits.append(rabbit(age, food, pos, rabbit.speed, lbreed))

        for f in range(nf):
            pos = floc[f, :]
            age = np.ceil(rand()*10)
            food = np.ceil(rand()*20)+20
            lbreed = np.round(rand()*fox.brdfq)
            self.foxes.append(fox(age, food, pos, fox.speed, lbreed))