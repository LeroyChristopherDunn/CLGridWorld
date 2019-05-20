from abc import abstractmethod
from typing import Union, Iterable

import numpy as np


class Policy:

    def __init__(self):
        self.episode = 0

    @abstractmethod
    def select_action(self, q_values) -> int:
        pass

    def inc_episode(self):
        self.episode += 1


class EpsGreedy(Policy):

    def __init__(self, eps=0.1):
        super().__init__()
        self.eps = eps

    def select_action(self, q_values: Union[np.ndarray, Iterable, int, float]) -> int:

        assert q_values.ndim == 1
        nb_actions = q_values.shape[0]

        if np.random.uniform() < self.eps:
            action = np.random.random_integers(0, nb_actions - 1)
        else:
            action = np.argmax(q_values)

        return action


class EpsAnnealed(Policy):

    def __init__(self, num_decay_episodes):
        super().__init__()
        self.eps = 1
        self.num_decay_episodes = num_decay_episodes

    def inc_episode(self):
        super().inc_episode()
        half_num_episodes = self.num_decay_episodes / 2
        self.eps = 1.0 * half_num_episodes / (half_num_episodes + self.episode)
        if self.episode % 100 == 0:
            print(self.eps)

    def select_action(self, q_values: Union[np.ndarray, Iterable, int, float]) -> int:

        assert q_values.ndim == 1
        nb_actions = q_values.shape[0]

        if np.random.uniform() < self.eps:
            action = np.random.random_integers(0, nb_actions - 1)
        else:
            action = np.argmax(q_values)

        return action
