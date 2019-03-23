import time

import matplotlib.pyplot as plt
import numpy as np
from gym import logger

from clgridworld.grid_world_action import GridWorldAction
from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams


class QLearningEpsilonDecreasingAgent:

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

    def get_action(self, curr_state, should_log=False):

        if np.random.rand(1) < self.epsilon:
            # exploration
            if should_log:
                print("taking random action - exploration")
            return self.action_space.sample()
        else:
            # exploitation
            if curr_state not in self.Q:
                self.Q[curr_state] = np.zeros([self.num_actions])
            if should_log:
                print("taking best action - exploitation")
            return np.argmax(self.Q[curr_state])

    def update(self, prev_state, action, curr_state, reward):

        if curr_state not in self.Q:
            self.Q[curr_state] = np.zeros([self.num_actions])

        self.Q[prev_state][action] += self.alpha * (reward + self.gamma * np.max(self.Q[curr_state]) - self.Q[prev_state][action])


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
    agent = QLearningEpsilonDecreasingAgent(env.action_space, discount_factor=1, seed=seed)

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

        episodic_rewards.append(accum_reward)
        agent.inc_episode()
        if i % 100 == 0:
            avg_reward = np.average(episodic_rewards[-100:])
            print("episode {} avg reward: {}".format(i, avg_reward))

    plt.plot(episodic_rewards)
    plt.ylabel('Episodic Reward')
    plt.xlabel('Episode')
    plt.show()

    env.close()
