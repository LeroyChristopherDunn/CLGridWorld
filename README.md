# CLGridWorld
Configurable Curriculum Learning Domain for Reinforcement Learning Agents

- [Curriculum Learning](#curriculum-learning)
- [Grid World Domain](#grid-world-domain)
- [Installation](#installation)
- [Grid World Generation](#grid-world-generation)
  * [Degrees of freedom](#degrees-of-freedom)
  * [Rules](#rules)
- [Basic Usage](#basic-usage)
  * [Grid World Generation](#grid-world-generation-1)
    + [Complete Spec (key, lock, and pit)](#complete-spec--key--lock--and-pit-)
    + [Key Only](#key-only)
    + [Lock and Pit](#lock-and-pit)
  * [Example Agents](#example-agents)
- [Gym Environment](#gym-environment)
  * [Observations, State Space](#observations--state-space)
  * [Action Space](#action-space)
- [Todo](#todo)
- [Contributing](#contributing)
- [Running the Tests](#running-the-tests)
- [Authors](#authors)
- [License](#license)
- [References](#references)

# Curriculum Learning

Quoted directly from [1]

"As reinforcement learning (RL) agents are challenged to learn increasingly complex tasks, some of these tasks may be in-feasible to learn directly. Various transfer learning methods and frameworks have been proposed that allow an agent to better learn a difficult target task by levering knowledge gained in one or more source tasks [Taylor and Stone, 2009;Lazaric, 2011]. Recently, these ideas have been extended to the problem of curriculum learning, where the goal is to design a curriculum consisting of a sequence of training tasks that are learned by the agent prior to learning the target task."

# Grid World Domain

Quoted directly from [1]

![GridWorld](img/GridWorld.PNG)

"The world consists of a room, which can contain 4 types of objects. Keys are items the agent can pick up by moving to them and executing a pickup action. These are used to unlock locks. Each lock in a room is dependent on a set of keys. If the agent is holding the right keys, then moving to a lock and executing an unlock action opens the lock. Pits are obstacles placed throughout the domain. If the agent moves into a pit, the episode is terminated. Finally, beacons are landmarks that are placed on the corners of pits. 

The goal of the learning agent is to traverse the world and unlock all the locks. At each time step, the learning agent can move in one of the four cardinal directions, execute a pickup action, or an unlock action. Moving into a wall causes no motion. Sucessfully picking up a key gives a reward of +500, and sucessfully unlocking a lock gives a reward of +1000. Falling into a pit terminates the episode with a reward of -200. All other actions receive a constant step penalty of -10."

# Installation

Compatible with python 3.7 and upwards

```bash
git clone https://github.com/LeroyChristopherDunn/CLGridWorld.git
cd CLGridWorld
pip install -e .
```

# Grid World Generation

The GridWorldGenerator can be used to create a variety of grid worlds. All generated grid worlds subclass the gym.Env class from ![openaigym](https://github.com/openai/gym/blob/master/README.rst) and therefore can be used in a plug-and-play fashion with various rl agents developed by the community

## Degrees of freedom

Currently the CL grid world has the following degrees of freedom:

- grid size
- player start location
- key location (optional)
- lock location (optional)
- pit start location (optional)
- pit end location (optional)

The degrees of freedom marked as optional, can be excluded from an generated grid world. For instance, a grid world may be created with or without a pit. 

## Rules

In it's standard form, an episode ends when an agent collects all keys and unlocks all locks. If the lock location is not specified to the grid world generator, a grid world without a lock will be generated and the episode will end when the agent collects all keys. If the key location is not specified to the grid generator, a grid world without a key will be generated and the agent will begin the episode with all keys. Either key location, lock location, or both must be passed to the grid world generator. 

Pit start location and end location define the starting and end points of the pit rectangle. Either both locations must be passed to the grid world generator to create a grid world with a pit, or both excluded to created a grid world without a pit.

# Basic Usage

## Grid World Generation

Below are code snippets to generate grid worlds with varying features

### Complete Spec (key, lock, and pit)

![Complete Spec](img/GridWorld_complete_spec.PNG)

```python
from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams

params = InitialStateParams(shape=(10, 10), player=(1, 4), key=(7, 5), lock=(1, 1), pit_start=(4, 2),
                            pit_end=(4, 7))    
env = GridWorldBuilder.create(params)
```

### Key Only

![Key Only](img/GridWorld_key_only.PNG)

```python
from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams

params = InitialStateParams(shape=(5, 5), player=(4, 4), key=(0, 0))
env = GridWorldBuilder.create(params)
```

### Lock and Pit

![Key Only](img/GridWorld_lock_and_pit.PNG)

```python
from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams

params = InitialStateParams(shape=(7, 7), player=(6, 5), lock=(0, 1), pit_start=(3, 2), pit_end=(3, 6))
env = GridWorldBuilder.create(params)
```

## Example Agents

See the ``examples`` directory.

- Run ![examples/agents/random_agent.py](example/agents/random_agent.py) to run an simple random agent.
- Run ![examples/agents/q_learning eps_greedy_agent](example/agents/q_learning_eps_greedy_agent.py) to run a basic q learning agent with epsilon greedy exploration
- Run ![examples/agents/q_learning_eps_dec_agent](example/agents/q_learning_eps_dec_agent.py) to run a basic q learning agent wiht epsilon decreasing exploration

# Gym Environment

## Observations, State Space

Each observation is a dictionary with the keys defined below:

| Key       | Type             | Nullable ('None') |
|-----------|------------------|-------------------|
| grid_size | tuple (int, int) |                   |
| player    | tuple (int, int) |                   |
| lock      | tuple (int, int) |         x         |
| key       | tuple (int, int) |         x         |
| pit_start | tuple (int, int) |         x         |
| pit_end   | tuple (int, int) |         x         |
| nw_beacon | tuple (int, int) |         x         |
| ne_beacon | tuple (int, int) |         x         |
| sw_beacon | tuple (int, int) |         x         |
| se_beacon | tuple (int, int) |         x         |
| has_key   | boolean 0 or 1   |                   |

For example to retrieve the player coords from the observation

```python
player = observation["player"]
```

## Action Space

| Key | Description |
|-----|-------------|
| 0   | North       |
| 1   | East        |
| 2   | South       |
| 3   | West        |
| 4   | Pick up key |
| 5   | Unlock lock |

# Todo

- Create environment wrappers to expose alternative observations, such as those described in [1]
- Pass additional parameters to grid world generator to configure the reward function
- Pass additional parameters to grid world generator to define 'empty space' terminal states

# Contributing

Please do

# Running the Tests

from the project root
```bash
python -m unittest 
```

# Authors

* **Leroy Dunn** - *Initial work* - [LeroyChristopherDunn](https://github.com/LeroyChristopherDunn)

# License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details

# References

[1] Narvekar, Sanmit, Jivko Sinapov, and Peter Stone. "Autonomous Task Sequencing for Customized Curriculum Design in Reinforcement Learning." IJCAI. 2017.


