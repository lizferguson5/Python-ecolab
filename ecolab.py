from agents import rabbit,fox
import environment
import numpy as np
from numpy.random import rand
import copy

def create_agents(nr, nf, env):
    """
    create_agents(nr, nf, env)

    Creates a list of agents within the environment env

    Input:

    nr - Integer: Number of rabbits
    nf - Integer: Number of foxes
    env - environment object: The environment in which to create the agents

    output:
    agent_list - Lists of generated agents


    """
    # We create the transpose here in order to generate matrices that are identical to MATLAB's
    # generate random initial positions for rabbits and foxes

    rloc = np.transpose((env.bm_size-1)*rand(2, nr))+1
    floc = np.transpose((env.bm_size-1)*rand(2, nf))+1

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

    return(rabbits,foxes)

# def agent_solve(rabbit_list, fox_list,env):

#     new_rabbits = []  # List of new rabbits created for this iteration
#     for agent in rabbit_list:
#         eaten = agent.eat(env)
#         # If the rabbit hasn't eaten, migrate
#         if not eaten:
#             agent.migrate(env)

#     # Remove rabbits that are ready to die
#     rabbit_list = [r for r in rabbit_list if not r.die()]

#     # Rabbits that are still alive might breed
#     for agent in rabbit_list:
#              new = agent.breed()
#              if isinstance(new, rabbit):
#                  new_rabbits.append(new)
    
#     # # Add new rabbits to list
#     rabbit_list.extend(new_rabbits)

#     new_foxes = []  # List of new rabbits created for this iteration
#     for agent in fox_list:
#         eaten = agent.eat(rabbit_list)
#         # If the fox hasn't eaten, migrate
#         if not eaten:
#             agent.migrate(env)

#     # Remove foxes that are ready to die
#     fox_list = [f for f in fox_list if not f.die()]

#     # foxes that are still alive might breed
#     for agent in fox_list:
#              new = agent.breed()
#              if isinstance(new, fox):
#                  new_foxes.append(new)
    
#     # Add new foxes to list
#     fox_list.extend(new_foxes)

#     return(rabbit_list,fox_list)

def agent_solve_matlab(agent_list,env):
    new_agents = []  # List of new agents created for this iteration
    
    # Created to emulate the possibly buggy behaviour in the MATLAB version
    for agent in agent_list:
        agent.old_pos = agent.pos

    for agent in agent_list:
            if isinstance(agent,rabbit):
                eaten = agent.eat(env)
            else:
                eaten = agent.eat(agent_list) # emulates original behaviour

            # If the agent hasn't eaten, migrate
            if not eaten:
                agent.migrate(env)

            # Apply the death rule - from starvation or old age
            agent.die()
            
            if not agent.dead:
                new = agent.breed()
                if new is not None:
                    new_agents.append(new)
            
    # Add new agents to list
    agent_list.extend(new_agents)
            
    # Remove agents that are ready to die
    agent_list = [a for a in agent_list if not a.dead and not a.has_been_eaten] 


    return(agent_list)

def ecolab_matlab(size, nr, nf, steps):
    #Works on a single list of rabbits and foxes like MATLAB did
    env = environment.environment(size)
    (rabbits,foxes) = create_agents(nr,nf,env)

    rabbits.extend(foxes)
    agents = rabbits

    history = np.zeros((2,steps))

    for n_it in range(steps):
        # print("{1} I haz {0} agents".format(len(agents),n_it+1))
        rabbits = [a for a in agents if isinstance(a,rabbit)]
        foxes = [a for a in agents if isinstance(a,fox)]
        # print("    I haz {0} f {1} r".format(len(foxes),len(rabbits),n_it+1))

        # # for agent in rabbits:
        # #      print("I am a {0} at {1},{2}".format(agent.__class__.__name__,agent.pos[0],agent.pos[1]))
        history[0,n_it] = len(rabbits)
        history[1,n_it] = len(foxes)

        (agents) = agent_solve_matlab(agents,env)  

    return(agents,env,history)

def ecolab(size, nr, nf, steps):
    env = environment.environment(size)
    (rabbits,foxes) = create_agents(nr,nf,env)

    for n_it in range(steps):
        print("{1} I haz {0} rabbits".format(len(rabbits),n_it))
        print("{1} I haz {0} foxes".format(len(foxes),n_it))

        (rabbits,foxes) = agent_solve(rabbits,foxes,env)

    return(rabbits,foxes,env)