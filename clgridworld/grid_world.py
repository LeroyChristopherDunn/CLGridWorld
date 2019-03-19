import gym


class GridWorld(gym.Env):

    def __init__(self, observation_space, action_space, initial_state, reward_function, dynamics,
                 terminal_state_validator, visualizer):

        self.initial_state = initial_state
        self.observation_space = observation_space
        self.action_space = action_space
        self.dynamics = dynamics
        self.reward_function = reward_function
        self.terminal_state_validator = terminal_state_validator
        self.visualizer = visualizer

        # self.reward_range = reward_function.reward_range

        self.prev_state = self.initial_state
        self.curr_state = self.initial_state

    def step(self, action):
        self.prev_state = self.curr_state
        self.curr_state = self.dynamics.step(self.prev_state, action)
        reward = self.reward_function.calculate(self.prev_state, action, self.curr_state)
        done = self.terminal_state_validator.is_terminal_state(self.curr_state)
        info = {}
        return self.curr_state, reward, done, info

    def reset(self):
        self.prev_state = self.initial_state
        self.curr_state = self.initial_state
        return self.initial_state

    def render(self, mode='human'):
        self.visualizer.render(self.curr_state)

    def seed(self, seed=None):
        self.observation_space.seed(seed)
        self.action_space.seed(seed)
