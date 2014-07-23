from agents import rabbit,fox
import environment
import numpy as np
from numpy.random import rand
import copy

def agent_solve_matlab(env):
    new_agents = []  # List of new agents created for this iteration
    
    # Update old_pos in each agent so that it contains position from previous iteration
    for agent in env.agents:
        agent.old_pos = agent.pos

    for agent in env.agents:
            eaten = agent.eat(env)

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
    env.agents.extend(new_agents)
            
    # Remove agents that are ready to die
    env.agents = [a for a in env.agents if not a.dead and not a.has_been_eaten] 

def ecolab_matlab(size, nr, nf, steps):
    env = environment.environment(size)
    env.create_agents(nr,nf,'joined')

    history = np.zeros((2,steps))

    for n_it in range(steps):
        rabbits = [a for a in env.agents if isinstance(a,rabbit)]
        foxes = [a for a in env.agents if isinstance(a,fox)]

        history[0,n_it] = len(rabbits)
        history[1,n_it] = len(foxes)

        agent_solve_matlab(env)  

    return(env.agents,env,history)