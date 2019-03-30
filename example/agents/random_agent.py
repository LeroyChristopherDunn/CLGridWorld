from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams

from example.agent_trainer import AgentTrainer
from example.agents.agent import Agent


class RandomAgent(Agent):
    """The world's simplest agent!"""

    def __init__(self, action_space):
        self.action_space = action_space

    def get_action(self, curr_state):
        self.action_space.sample()

    def update(self, prev_state, action, curr_state, reward):
        pass

    def inc_episode(self):
        pass

    def get_best_action(self, curr_state):
        return self.get_action(curr_state)


if __name__ == '__main__':

    params = InitialStateParams(shape=(10, 10), player=(1, 4), lock=(9, 1))
    env = GridWorldBuilder.create(params)
    seed = 0
    agent = RandomAgent(env.action_space)

    AgentTrainer(env, agent).train(seed, num_episodes=100, max_steps_per_episode=5000, episode_log_interval=1)
