from abc import abstractmethod

import numpy as np


class Agent:

    @abstractmethod
    def get_action(self, curr_state):
        pass

    @abstractmethod
    def update(self, prev_state, action, curr_state, reward):
        pass

    @abstractmethod
    def inc_episode(self):
        pass

    @abstractmethod
    def get_best_action(self, curr_state):
        pass

    def make_hashable(self, state):
        if isinstance(state, np.ndarray):
            return tuple(state)

        return state

