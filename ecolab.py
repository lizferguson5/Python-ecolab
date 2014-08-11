from agents import rabbit, fox
import environment
import numpy as np
from messages import message

def update_messages(env):
        # Update messages for each agent
        for agent in env.agents:
            agent.process_messages(env)

        # Clean up the dead
        num_rabbit_dead = 0
        num_foxes_dead = 0
        
        for agent in env.agents:
            if isinstance(agent, rabbit) and (agent.messages.dead or agent.messages.has_been_eaten):
                num_rabbit_dead = num_rabbit_dead + 1
            if isinstance(agent, fox) and (agent.messages.dead or agent.messages.has_been_eaten):
                num_foxes_dead = num_foxes_dead + 1


        # Create new list that only contains the living
        env.agents = ([a for a in env.agents if not a.messages.dead and
                      not a.messages.has_been_eaten])

        # Update counters
        rabbit.num_rabbits = rabbit.num_rabbits - num_rabbit_dead
        fox.num_foxes = fox.num_foxes - num_foxes_dead



def agent_solve(env):
    """Runs one iteration of the simulation.
    """
    new_agents = []  # List of new agents created for this iteration

    if env.mode == 'sync':
        # Apply rules
        for agent in env.agents:
            eaten = agent.eat(env)

            # If the agent hasn't eaten, migrate
            if not eaten:
                agent.migrate(env)

            # Apply the death rule - from starvation or old age
            agent.die(env)

            # If the agent did not die, apply the breed rule
            if not agent.messages.dead:
                new = agent.breed(env)
                if new is not None:
                    new_agents.append(new)

        # Add new agents to list
        env.agents.extend(new_agents)

        # Update messages
        update_messages(env)

    if env.mode == 'async':
        # Apply rules
        for agent in env.agents:
            eaten = agent.eat(env)

            # If the agent hasn't eaten, migrate
            if not eaten:
                agent.migrate(env)

            # Apply the death rule - from starvation or old age
            agent.die(env)

            # If the agent did not die, apply the breed rule
            if not agent.dead:
                new = agent.breed(env)
                if new is not None:
                    new_agents.append(new)

        # Add new agents to list
        env.agents.extend(new_agents)

        # Clean up the dead
        env.agents = ([a for a in env.agents if not a.dead and
                      not a.has_been_eaten])


def ecolab(size, nr, nf, steps, mode='sync'):
    """ecolab - Python version of the original MATLAB code by Dawn Walker.
    Python version by Mike Croucher.

    Parameters
    ----------

    size : integer
        The length of one side of the square of the environment in which the
        agents live.

    nr: integer
        Initial Number of rabbits

    nf: integer
        Initial number of foxes

    steps: integer
        Number of simulation steps

    mode: string (default='sync')
        Simulation mode, either 'sync' or 'async'
        'sync' - Agents use information on previous iteration on which to
        base their decisions. This gives the same results as the MATLAB original.
        Some unphysical events can occur such as a dead rabbit giving birth

        'async' - Agents always use the most up to date information on which
        to base their decsisons.

    """
    #Ensure that numbers of rabbits and foxes are zero'd for this simulation
    rabbit.num_rabbits = 0
    fox.num_foxes = 0

    env = environment.environment(size, mode)
    env.create_agents(nr, nf, 'joined')

    history = np.zeros((2, steps))

    for n_it in range(steps):
        history[0, n_it] = rabbit.num_rabbits
        history[1, n_it] = fox.num_foxes

        agent_solve(env)

    return(env.agents,env,history)