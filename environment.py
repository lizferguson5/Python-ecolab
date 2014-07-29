import numpy as np
from agents import rabbit, fox
from numpy.random import rand


class environment:
    """An environment contains the area in which the agents live along
       with the agents themselves.

       Various model parameters such as simulation mode ('sync or 'async')
       are also stored here.
    """

    def __init__(self, size, mode='sync'):
        self.bm_size = size

        # distribute food - 50 per square
        self.food = np.floor(50 * np.ones((size, size)))

        # generate patch where there is no food
        self.food[np.round(0.6 * size)-1:np.round(0.8*size),
                  np.round(0.6*size)-1:np.round(0.8*size)] = 0

        # Is this model synchronous or asynchronous?
        self.mode = mode

    def create_agents(self, nr, nf, list_type='joined'):
        """
        environment.create_agents(nr, nf) - Creates a list of agents
        within the environment

        Input Parameters
        ----------------

        nr : integer
            Number of rabbits

        nf : integer
            Number of foxes

        list_type : string (default='joined')
            Determines how the agents are stored.
                    'joined' - maintains a single list containing both
                    rabbits and foxes.

                    'seprate' - maintains separate lists of rabbits and foxes
                    (THIS WONT WORK WITH THE REST OF ECOLAB YET)


        Output:
        -------

        agent_list : list
            List(s) of generated agents


        """
        # We create the transpose here in order to generate matrices
        # that are identical to MATLAB's
        # generate random initial positions for rabbits and foxes
        rloc = np.transpose((self.bm_size-1)*rand(2, nr))+1
        floc = np.transpose((self.bm_size-1)*rand(2, nf))+1

        rabbits = []
        foxes = []

        for r in range(nr):
            pos = rloc[r, :]
            age = np.ceil(rand()*10)
            food = np.ceil(rand()*20)+20
            lbreed = np.round(rand()*rabbit.brdfq)
            rabbits.append(rabbit(age, food, pos, rabbit.speed, lbreed))

        for f in range(nf):
            pos = floc[f, :]
            age = np.ceil(rand()*10)
            food = np.ceil(rand()*20)+20
            lbreed = np.round(rand()*fox.brdfq)
            foxes.append(fox(age, food, pos, fox.speed, lbreed))

        if list_type == 'separate':
            self.foxes = foxes
            self.rabbits = rabbits
        elif list_type == 'joined':
            self.agents = rabbits
            self.agents.extend(foxes)