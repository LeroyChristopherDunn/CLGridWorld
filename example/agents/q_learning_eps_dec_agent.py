import numpy as np

from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams
from example.agent_trainer import AgentTrainer
from example.agents.agent import Agent


class QLearningEpsilonDecreasingAgent(Agent):

    def __init__(self, action_space, discount_factor=0.95, learning_rate=0.01, epsilon=0.1, seed=None):

        self.num_actions = action_space.n

        np.random.seed(seed)

        self.Q = {}
        self.action_space = action_space

        self.gamma = discount_factor
        self.alpha = learning_rate
        self.epsilon = epsilon

        self.episode_count = 1

    def update_epsilon(self):
        self.epsilon = 500.0 / (500.0 + self.episode_count)

    def inc_episode(self):
        self.episode_count += 1
        self.update_epsilon()

    def get_action(self, curr_state):

        if np.random.rand(1) < self.epsilon:
            # exploration
            return self.action_space.sample()
        else:
            # exploitation
            return self.get_best_action(curr_state)

    def get_best_action(self, curr_state):
        if curr_state not in self.Q:
            self.Q[curr_state] = np.zeros([self.num_actions])
        return np.argmax(self.Q[curr_state])

    def update(self, prev_state, action, curr_state, reward):

        if curr_state not in self.Q:
            self.Q[curr_state] = np.zeros([self.num_actions])

        self.Q[prev_state][action] += self.alpha * (reward + self.gamma * np.max(self.Q[curr_state]) - self.Q[prev_state][action])


if __name__ == '__main__':

    seed = 0

    # target task spec as defined in Source Task Sequencing,,, Narvekar et al 2017
    params = InitialStateParams(shape=(10, 10), player=(1, 4), key=(7, 5), lock=(1, 1), pit_start=(4, 2),
                                pit_end=(4, 7))
    env = GridWorldBuilder.create(params)

    agent = QLearningEpsilonDecreasingAgent(env.action_space, discount_factor=1, seed=seed)

    AgentTrainer(env, agent).train(seed, num_episodes=5000, max_steps_per_episode=10000, episode_log_interval=100)

