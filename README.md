# CLGridWorld
Configurable Curriculum Learning Domain for Reinforcement Learning Agents. As specified by [1]

# Curriculum Learning

Quoted directly from [1]

"As reinforcement learning (RL) agents are challenged to learn increasingly complex tasks, some of these tasks may be in-feasible to learn directly. Various transfer learning methods and frameworks have been proposed that allow an agent to better learn a difficult target task by levering knowledge gained in one or more source tasks [Taylor and Stone, 2009;Lazaric, 2011]. Recently, these ideas have been extended to the problem of curriculum learning, where the goal is to design a curriculum consisting of a sequence of training tasks that are learned by the agent prior to learning the target task."

# Grid World Domain

Quoted directly from [1]

"The world consists of a room, which can contain 4 types of objects. Keys are items the agent can pick up by moving to them and executing a pickup action. These are used to unlock locks. Each lock in a room is dependent on a set of keys. If the agent is holding the right keys, then moving to a lock and executing an unlock action opens the lock. Pits are obstacles placed throughout the domain. If the agent moves into a pit, the episode is terminated. Finally, beacons are landmarks that are placed on the corners of pits. 

The goal of the learning agent is to traverse the world and unlock all the locks. At each time step, the learning agent can move in one of the four cardinal directions, execute a pickup action, or an unlock action. Moving into a wall causes no motion. Sucessfully picking up a key gives a reward of +500, and sucessfully unlocking a lock gives a reward of +1000. Falling into a pit terminates the episode with a reward of -200. All other actions receive a constant step penalty of -10."

# Grid World Generation



# Installation

```bash
git clone https://github.com/LeroyChristopherDunn/CLGridWorld.git
cd CLGridWorld
pip install -e .
```

# Basic Usage

# Todo

# References

[1] Narvekar, Sanmit, Jivko Sinapov, and Peter Stone. "Autonomous Task Sequencing for Customized Curriculum Design in Reinforcement Learning." IJCAI. 2017.


