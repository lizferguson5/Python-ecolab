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
    # First, how many have been eaten? 
    # We need to do it here since rabbits can be eaten twice
    # This could be simplified if we stop using last_pos in the eat functions -- something we are doing to emulate the MATLAB results
    num_rabbit_eaten = 0
    for agent in env.agents:
        if isinstance(agent,rabbit) and agent.has_been_eaten and not agent.dead:
            num_rabbit_eaten = num_rabbit_eaten + 1
    # Remove eaten and dead from the list of agents
    env.agents = [a for a in env.agents if not a.dead and not a.has_been_eaten]

    # The Dead are automatically accounted for in the .die() functions
    # Only need to decrement total number of eaten 
    rabbit.num_rabbits = rabbit.num_rabbits - num_rabbit_eaten

def ecolab_matlab(size, nr, nf, steps):
    env = environment.environment(size)
    env.create_agents(nr,nf,'joined')

    history = np.zeros((2,steps))

    for n_it in range(steps):
        history[0,n_it] = rabbit.num_rabbits
        history[1,n_it] = fox.num_foxes

        agent_solve_matlab(env)  

    return(env.agents,env,history)