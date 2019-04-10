from types import SimpleNamespace
from typing import NamedTuple, Optional, Tuple

from clgridworld.grid_world import GridWorld
from clgridworld.action.action import GridWorldActionSpace
from clgridworld.dynamics.dynamics import GridWorldDynamics
from clgridworld.state.validator import TerminalStateValidator
from clgridworld.visualizer.grid_state_visualizer import GridStateVisualizer
from clgridworld.reward.reward import GridWorldRewardFunction
from clgridworld.state.state import GridWorldObservationSpace, GridWorldState
from clgridworld.state.state_factory import GridWorldStateFactory


class InitialStateParams(NamedTuple):

    shape: Tuple[int, int]
    player: Tuple[int, int]
    key: Optional[Tuple[int, int]] = None
    lock: Optional[Tuple[int, int]] = None
    pit_start: Optional[Tuple[int, int]] = None
    pit_end: Optional[Tuple[int, int]] = None


class GridWorldBuilder:

    @staticmethod
    def create(params: InitialStateParams) -> GridWorld:

        initial_state = GridWorldStateFactory.create(params.shape, params.player, params.key,
                                                     params.lock, params.pit_start, params.pit_end)

        observation_space = GridWorldObservationSpace(params.shape)
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
        grid_state = GridStateVisualizer(curr_state)
        print(grid_state.grid)
        has_key = "true" if grid_state.state.has_key else "false"
        print("has_key: " + has_key)



