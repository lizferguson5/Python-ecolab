from agents import rabbit,fox
import environment
import numpy as np
from numpy.random import rand
import copy

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
    env.create_agents(nr,nf)

    env.rabbits.extend(env.foxes)
    agents = env.rabbits

    history = np.zeros((2,steps))

    for n_it in range(steps):
        rabbits = [a for a in agents if isinstance(a,rabbit)]
        foxes = [a for a in agents if isinstance(a,fox)]

        history[0,n_it] = len(rabbits)
        history[1,n_it] = len(foxes)

        (agents) = agent_solve_matlab(agents,env)  

    return(agents,env,history)