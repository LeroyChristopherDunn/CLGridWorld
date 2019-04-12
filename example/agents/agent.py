from abc import abstractmethod

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
