Python-ecolab
=============

Python port of Dawn Walker's ecolab code.

### Files list

* **agents.py** - Definitions of the fox and rabbit classes
* **ecolab.py** - The ecolab and agent\_solve functions.
* **environment.py** - Definition of the environment class. An environment is the area in which agents live and the agents that live in it.
* **fox\_rabbit\_20\_60\_5.mat** - Results from running the MATLAB version of ecolab(20,60,5,200)
* **run_simulation.py** - Example simulation.
* **unittests.py** - Unit tests

### The Ecolab function

The ecolab function has two modes, 'async' and 'sync'.

* 'sync' - all agents update synchronously (all agents only have access to the information from the previous time step). This emulates the behaviour of the MATLAB original

* 'async' - All agents have access to the most up to date information at all times.

For example

`(agents,env,history) = ecolab.ecolab(size=20, nr=200, nf=30, steps=100, 	mode='sync')`

* agents - List of agents left after simulation ends
* env - End state of the environment
* history - A matrix containing the historical numbers of rabbits and foxes

**Note: While writing this doc, it occured to me that returning the list of agents and the environment is pointless since the environment contains the agents. Will update later.**

### Example

Run the file **run\_simulation.py**. This runs the same simulation twice, once in async mode and once in sync mode.  The results are saved as .csv files and plotting as .png files

