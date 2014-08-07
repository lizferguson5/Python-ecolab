class message:
    """
    Class representing messages passed to agents. 

    Each agent contains its own message class which represents messages passed to it. 
    """
    def __init__(self, pos=[], dead=[], has_been_eaten=[]):
        self.pos = pos
        self.dead = dead
        self.has_been_eaten = has_been_eaten
