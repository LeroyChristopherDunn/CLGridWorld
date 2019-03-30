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

    def update(self, prev_state, prev_action, prev_reward, curr_state, curr_action):

        if curr_state not in self.Q:
            self.Q[curr_state] = np.zeros([self.num_actions])

        self.Q[prev_state][prev_action] += self.alpha * (prev_reward + self.gamma * self.Q[curr_state][curr_action]
                                                         - self.Q[prev_state][prev_action])


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

        done = False
        next_state = env.reset()
        curr_state = None
        curr_action = None
        curr_reward = 0
        step_count = 0
        accum_reward = 0

        while True:

            prev_state = curr_state
            curr_state = next_state
            prev_action = curr_action
            prev_reward = curr_reward

            curr_action = agent.get_action(curr_state)
            next_state, curr_reward, done, _ = env.step(curr_action)

            if prev_state is not None and prev_action is not None:
                agent.update(prev_state, prev_action, prev_reward, curr_state, curr_action)

            step_count += 1
            accum_reward += curr_reward

            ## uncomment the below lines to render the environment to terminal
            # env.render()
            # print("episode: " + str(i) + "." + str(step_count))
            # print("action: " + GridWorldAction.NAMES[curr_action])
            # print("reward: " + str(curr_reward))
            # print("accum reward: " + str(accum_reward))
            # print("epsilon: " + str(agent.epsilon))
            # print("\n")
            # time.sleep(0.5)

            if done or step_count >= max_steps_per_episode:
                # don't forget to update terminal state reward
                agent.update(curr_state, curr_action, curr_reward, next_state, agent.get_best_action(next_state))
                break

        episodic_rewards.append(accum_reward)
        if i % 100 == 0:
            avg_reward = np.average(episodic_rewards[-100:])
            print("episode {} avg reward: {}".format(i, avg_reward))

    plt.plot(episodic_rewards)
    plt.ylabel('Episodic Reward')
    plt.xlabel('Episode')
    plt.show()

    env.close()
