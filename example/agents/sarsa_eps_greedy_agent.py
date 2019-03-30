import time

import numpy as np
import matplotlib.pyplot as plt

from clgridworld.grid_world_action import GridWorldAction
from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams
from gym import logger


class SarsaEpsilonGreedyAgent:

    def __init__(self, action_space, discount_factor=0.95, learning_rate=0.01, epsilon=0.1, seed=0):

        self.num_actions = action_space.n

        np.random.seed(seed)

        self.Q = {}
        self.action_space = action_space

        self.gamma = discount_factor
        self.alpha = learning_rate
        self.epsilon = epsilon

        self.prev_sample = None

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

        if self.prev_sample is not None:
            prev_sample = self.prev_sample
            self._update(prev_sample[0], prev_sample[1], prev_sample[2], prev_sample[3], action)

        self.prev_sample = (prev_state, action, curr_state, reward)

    def _update(self, prev_state, prev_action, curr_state, prev_reward, curr_action):

        if curr_state not in self.Q:
            self.Q[curr_state] = np.zeros([self.num_actions])

        self.Q[prev_state][prev_action] += self.alpha * (prev_reward + self.gamma * self.Q[curr_state][curr_action]
                                                         - self.Q[prev_state][prev_action])

    def inc_episode(self):
        if self.prev_sample is not None:
            prev_sample = self.prev_sample
            self._update(prev_sample[0], prev_sample[1], prev_sample[2], prev_sample[3],
                         self.get_best_action(prev_sample[2]))


if __name__ == '__main__':

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    # target task spec as defined in Source Task Sequencing,,, Narvekar et al 2017
    params = InitialStateParams(shape=(10, 10), player=(1, 4), key=(7, 5), lock=(1, 1), pit_start=(4, 2),
                                pit_end=(4, 7))
    env = GridWorldBuilder.create(params)

    seed = 0
    env.seed(seed)
    agent = SarsaEpsilonGreedyAgent(env.action_space, discount_factor=1, seed=seed)

    print("Generated environment: ")
    env.render()
    print("")

    num_episodes = 5000
    max_steps_per_episode = 10000
    episodic_rewards = []

    for i in range(num_episodes):

        reward = 0
        done = False
        curr_state = env.reset()
        step_count = 0
        accum_reward = 0

        while True:

            prev_state = curr_state
            action = agent.get_action(curr_state)
            curr_state, reward, done, _ = env.step(action)
            agent.update(prev_state, action, curr_state, reward)

            step_count += 1
            accum_reward += reward

            ## uncomment the below lines to render the environment to terminal
            # env.render()
            # print("episode: " + str(i) + "." + str(step_count))
            # print("action: " + GridWorldAction.NAMES[action])
            # print("reward: " + str(reward))
            # print("accum reward: " + str(accum_reward))
            # print("epsilon: " + str(agent.epsilon))
            # print("\n")
            # time.sleep(0.5)

            if done or step_count >= max_steps_per_episode:
                break

        agent.inc_episode()

        episodic_rewards.append(accum_reward)
        if i % 100 == 0:
            avg_reward = np.average(episodic_rewards[-100:])
            print("episode {} avg reward: {}".format(i, avg_reward))

    plt.plot(episodic_rewards)
    plt.ylabel('Episodic Reward')
    plt.xlabel('Episode')
    plt.show()

    env.close()
