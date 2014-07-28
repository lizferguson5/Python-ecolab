import numpy as np
from numpy.random import rand


class fox:
    # The following attributes will apply for all foxes
    speed = 5                # speed of movement - units per itn
    brdfq = 20               # breeding frequency - iterations
    minfood = 0                # minimum food threshhold before agent dies
    foodbrd = 10               # minimum food threshold for breeding
    maxage = 50               # maximum age allowed
    num_foxes = 0             # Number of alive foxes

    def __init__(self, age=[], food=[], pos=[], speed=[], last_breed=[]):
        # These attributes vary on a per-fox basis
        self.age = age
        self.food = food
        self.pos = pos
        self.speed = speed
        self.last_breed = last_breed
        self.dead = False                 # Is this agent dead or alive?
        self.has_been_eaten = False       # Has this agent been eaten?

        # Messages passed to this agent
        self.messages = {}

        # Incremenent number of alive foxes by one 
        self.__class__.num_foxes = self.__class__.num_foxes + 1

    def __repr__(self):
        out = ('Age : {0}\nFood : {1}\nPos : {2}\n\
               Speed: {3}\nlast_breed: {4}\n'.
               format(self.age, self.food, self.pos, self.speed,
                      self.last_breed))
        return(out)

    def breed(self):
        # Only breed if agent has enough food and enough time has elapsed
        # since last breeding
        new = None
        if self.food >= self.foodbrd and self.last_breed >= self.brdfq:
            new = fox(age=0, food=self.food / 2.0,
                      pos=self.pos,  speed=self.speed, last_breed=0)
            self.food = self.food / 2.0
            self.last_breed = 0
        else:
            self.last_breed = self.last_breed + 1
        self.age = self.age + 1
        return(new)

    def move_pos(self, new_pos):
        # Sets new position of fox
        self.pos = new_pos

    def find_food(self, env):
        # Get all positions of agents as a numpy array.
        # Foxes are given infinite distance so that they are never considered
        if env.mode =='sync':
        # syncronous mode - use position of rabbit from previous iteration
            pos_array = (np.array([agent.messages['old_pos'] if isinstance(agent, rabbit)
                       else [np.inf, np.inf] for agent in env.agents]))
        elif env.mode == 'async':
            pos_array = (np.array([agent.pos if isinstance(agent, rabbit)
                       else [np.inf, np.inf] for agent in env.agents]))
        # find squared distance between self and all positions in the araray
        pos_array = ((self.pos[0] - pos_array[:, 0])**2 +
                   (self.pos[1] - pos_array[:, 1])**2)
        # Find minimum
        index = np.argmin(pos_array)

        # If the minimum distance found points to a fox,
        # i.e. is infiite distance away, return -1
        if np.isinf(pos_array[index]):
                    index = -1
        return(np.sqrt(pos_array[index]), index)

    def eat(self, env):
        """
        eaten = eat(self, env)

        eaten is True if the fox eats. False otherwise
        """
        eaten = False
        (distance, nearest_rabbit_ind) = self.find_food(env)
        # probability that fox will kill rabbit is ratio of speed to distance

        if distance <= self.speed and nearest_rabbit_ind is not -1:
            pk = 1 - (distance / self.speed)

            if pk > rand():
                # Move to same position as rabbit
                self.pos = env.agents[nearest_rabbit_ind].messages['old_pos']
                # kill rabbit
                env.agents[nearest_rabbit_ind].has_been_eaten = True

                self.food = self.food + 2
                eaten = True

        self.food = self.food - 1
        return(eaten)

    def migrate(self, env):
        mig = False
        cnt = 1
        direc = rand()*2*np.pi
        npos = np.zeros(2)
        while not mig and cnt <= 8:
            npos[0] = self.pos[0] + self.speed * np.cos(direc)
            npos[1] = self.pos[1] + self.speed * np.sin(direc)
            # check that fox has not left edge of model - correct if so.
            if npos[0] < env.bm_size and npos[1] < env.bm_size and \
               npos[0] >= 1 and npos[1] >= 1:
                mig = True
            cnt = cnt+1
            direc = direc + (np.pi/4)

        if mig:
            self.move_pos(npos)

    def die(self):
        # fox.die(self)
        # foxes die if their food level reaches zero or
        # they are older than max_age
        if self.food <= self.minfood or self.age > self.maxage:
            self.dead = True
            self.__class__.num_foxes = self.__class__.num_foxes - 1


class rabbit:
    # The following attributes will apply for all rabbits
    speed = 2              # speed of movement - units per itn
    brdfq = 10             # breeding frequency - iterations
    minfood = 0              # minimum food threshhold before agent dies
    foodbrd = 10             # minimum food threshold for breeding
    maxage = 50               # maximum age allowed
    num_rabbits = 0         # Number of alive rabbits

    def __init__(self, age=[], food=[], pos=[], speed=[], last_breed=[]):
        # These attributes apply to individual rabbits
        self.age = age
        self.food = food
        self.pos = pos

        # cpos: round up position to nearest grid point
        self.cpos = np.round(pos).astype(np.int) - 1
        self.speed = speed
        self.last_breed = last_breed

        self.dead = False                # Is this agent dead or alive?
        self.has_been_eaten = False      # Has this agent been eaten?

        # Messages passed to this agent
        self.messages = {}

        # We've created a new instance so increment the counter
        self.__class__.num_rabbits = self.__class__.num_rabbits + 1

    def __repr__(self):
        out = 'Age : {0}\nFood : {1}\nPos : {2}\nSpeed: {3}\nlast_breed: {4}\n'.\
            format(self.age, self.food, self.pos, self.speed, self.last_breed)
        return(out)

    def breed(self):
        # Only breed if agent has enough food and enough time
        # has elapsed since last breeding

        new = None
        if self.food >= self.foodbrd and self.last_breed >= self.brdfq:
            new = rabbit(0, self.food/2.0, self.pos,  self.speed, 0)
            self.food = self.food/2.0
            self.last_breed = 0
        else:
            self.last_breed = self.last_breed + 1
        self.age = self.age + 1
        return(new)

    def move_pos(self, new_pos):
        # Sets new position of rabbit.
        self.pos = new_pos
        self.cpos = np.round(self.pos).astype(np.int) - 1

    def die(self):
        # rabbit.die(self)
        # rabbits die if their food level reaches zero or they
        # are older than maxage
        if self.food <= self.minfood or self.age > self.maxage:
            self.dead = True
            self.__class__.num_rabbits = self.__class__.num_rabbits - 1

    def eat(self, env):
        # obtain environment food level at current location
        pfood = env.food[self.cpos[0], self.cpos[1]]
        if pfood >= 1:  # if food exists at this location
            env.food[self.cpos[0], self.cpos[1]] \
                = env.food[self.cpos[0], self.cpos[1]] - 1
            self.food = self.food + 1
            eaten = 1
        else:
            self.food = self.food - 1
            eaten = 0  # flag tells rabbit to migrate
        return(eaten)

    def extract_local_food(self, env):
        if self.cpos[0] > env.bm_size - self.speed:
            xmax = env.bm_size
        else:
            xmax = int(self.cpos[0] + 1 + self.speed)

        if self.cpos[0] < self.speed + 1:
            xmin = 0
        else:
            xmin = int(self.cpos[0] + 1 - self.speed - 1)

        if self.cpos[1] > env.bm_size - self.speed:
            ymax = env.bm_size
        else:
            ymax = int(self.cpos[1] + self.speed + 1)

        if self.cpos[1] < self.speed + 1:
            ymin = 0
        else:
            ymin = int(self.cpos[1] - self.speed)

        loc_food = env.food[xmin:xmax, ymin:ymax]
        return(loc_food, xmin+1, ymin+1)

    def migrate(self, env):
        mig = False   # indicates whether rabbit has successfully migrated
        (loc_food, xmin, ymin) = self.extract_local_food(env)
        (xf, yf) = np.where(loc_food)  # Find where food is present
        npos = np.zeros(2)

        if xf.size != 0:
            xa = xmin + xf  # x co-ords of all squares containing food in range
            ya = ymin + yf  # y co-ords of all squares containing food in range
            csep = np.sqrt((xa - self.pos[0])**2 + (ya - self.pos[1])**2)

            nrst = np.argmin(csep)
            if csep[nrst] <= self.speed:
                nx = xa[nrst] + rand() - 0.5
                ny = ya[nrst] + rand() - 0.5
                npos = np.array([nx, ny])

                # If agent has left edge of model,  adjust slightly
                shft = np.where(npos > env.bm_size)
                npos[shft] = env.bm_size-rand()
                shft = np.where(npos <= 1)
                npos[shft] = 1+rand()
                mig = True

        if not(mig):
            # rabbit has been unable to find food,
            # so chooses a random direction to move in
            cnt = 1
            dir = rand() * 2*np.pi
            while not(mig) and cnt <= 8:
                npos[0] = self.pos[0] + self.speed * np.cos(dir)
                npos[1] = self.pos[1] + self.speed * np.sin(dir)
                # check that fox has not left edge of model - correct if so.
                if npos[0] < env.bm_size and npos[1] < env.bm_size and \
                   npos[0] >= 1 and npos[1] >= 1:
                    mig = True
                cnt = cnt + 1
                dir = dir + (np.pi/4)

        if mig:
            self.move_pos(npos)