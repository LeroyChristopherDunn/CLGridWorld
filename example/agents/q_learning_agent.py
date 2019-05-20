import numpy as np

from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams
from clgridworld.wrapper.distance_observation_wrapper import DistanceObservationWrapper
from clgridworld.wrapper.tuple_observation_wrapper import TupleObservationWrapper
from example.agent_trainer import AgentTrainer
from example.agents.agent import Agent
from example.agents.policy import Policy, EpsGreedy, EpsAnnealed


class QLearningAgent(Agent):

    def __init__(self, action_space, policy: Policy, discount_factor=0.95, learning_rate=0.01, seed=0):

        self.num_actions = action_space.n
        self.policy = policy
        self.test_policy = EpsGreedy(0)

        np.random.seed(seed)

        self.Q = {}
        self.action_space = action_space

        self.gamma = discount_factor
        self.alpha = learning_rate

    def get_action(self, curr_state):

        self.init_state(curr_state)

        return self.policy.select_action(self.Q[curr_state])

    def get_best_action(self, curr_state):

        self.init_state(curr_state)

        return self.test_policy.select_action(self.Q[curr_state])

    def update(self, prev_state, action, curr_state, reward):

        self.init_state(curr_state)

        self.Q[prev_state][action] += self.alpha * \
                                      (reward + self.gamma * np.max(self.Q[curr_state]) - self.Q[prev_state][action])

    def init_state(self, state):
        if state not in self.Q:
            self.Q[state] = np.zeros([self.num_actions])

    def inc_episode(self):
        self.policy.inc_episode()
        self.test_policy.inc_episode()


if __name__ == '__main__':
    seed = 0

    # target task spec as defined in Source Task Sequencing,,, Narvekar et al 2017
    params = InitialStateParams(shape=(10, 10), player=(1, 4), key=(7, 5), lock=(1, 1), pit_start=(4, 2),
                                pit_end=(4, 7))
    env = GridWorldBuilder.create(params)
    env = DistanceObservationWrapper(env)  # transform state space to distance based states
    env = TupleObservationWrapper(env)  # convert states to tuples to make hashable

    policy = EpsGreedy(0.1)
    # policy = EpsAnnealed(250)  # uncomment for annealed policy

    agent = QLearningAgent(env.action_space, policy, discount_factor=1, seed=seed)

    AgentTrainer(env, agent).train(seed, num_episodes=5000, max_steps_per_episode=10000, episode_log_interval=100)
