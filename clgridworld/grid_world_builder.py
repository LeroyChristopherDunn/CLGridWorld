from types import SimpleNamespace

from clgridworld.grid_world import GridWorld
from clgridworld.grid_world_action import GridWorldActionSpace
from clgridworld.grid_world_dynamics import GridWorldDynamics, TerminalStateValidator
from clgridworld.grid_world_grid_state import GridWorldGridState
from clgridworld.grid_world_reward import GridWorldRewardFunction
from clgridworld.grid_world_state import GridWorldStateFactory, GridWorldStateObservationSpace, GridWorldState


class InitialStateParams:

    def __init__(self, shape: (int, int), player: (int, int), key: (int, int)=None, lock: (int, int)=None,
                 pit_start: (int, int)=None, pit_end: (int, int)=None):

        self.shape = shape
        self.player = player
        self.key = key
        self.lock = lock
        self.pit_start = pit_start
        self.pit_end = pit_end


class GridWorldBuilder:

    @staticmethod
    def create(params: InitialStateParams) -> GridWorld:

        initial_state = GridWorldStateFactory.create(params.shape, params.player, params.key,
                                                     params.lock, params.pit_start, params.pit_end)

        observation_space = GridWorldStateObservationSpace()
        action_space = GridWorldActionSpace()

        dynamics = SimpleNamespace()
        dynamics.step = GridWorldBuilder.step
        reward_function = SimpleNamespace()
        reward_function.calculate = GridWorldBuilder.reward
        terminal_state_validator = TerminalStateValidator
        visualizer = SimpleNamespace()
        visualizer.render = GridWorldBuilder.render

        return GridWorld(observation_space, action_space, initial_state, reward_function, dynamics,
                         terminal_state_validator, visualizer)

    @staticmethod
    def step(state: GridWorldState, action) -> GridWorldState:
        return GridWorldDynamics(state).step(action)

    @staticmethod
    def reward(curr_state: GridWorldState, action, next_state: GridWorldState) -> int:
        return GridWorldRewardFunction().calculate(curr_state, next_state)

    @staticmethod
    def render(curr_state: GridWorldState) -> None:
        grid_state = GridWorldGridState(curr_state)
        print(grid_state.grid)
        has_key = "true" if grid_state.state.has_key else "false"
        print("has_key: " + has_key)



