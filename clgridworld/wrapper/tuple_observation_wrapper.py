import gym


class TupleObservationWrapper(gym.ObservationWrapper):

    def observation(self, observation):
        return tuple(observation)