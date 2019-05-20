from functools import lru_cache

import gym as gym
import numpy as np
from gym import spaces

from clgridworld.action.action import GridWorldAction
from clgridworld.dynamics.dynamics import GridWorldDynamics
from clgridworld.grid_world import GridWorld
from clgridworld.state.state import GridWorldState
from clgridworld.state.validator import TerminalStateValidator
from clgridworld.wrapper.euclidean_distance_calculator import EuclideanDistanceCalculator


class DistanceObservationWrapper(gym.ObservationWrapper):

    def __init__(self, env: GridWorld):

        super(DistanceObservationWrapper, self).__init__(env)

        max_coords = env.initial_state.grid_shape
        max_dist = EuclideanDistanceCalculator.distance((0, 0), max_coords)

        observation_space_low = np.zeros(shape=(17,))
        observation_space_high = np.zeros(shape=(17,))
        observation_space_high[0:12] = max_dist
        observation_space_high[12:17] = 1

        self.observation_space = spaces.Box(low=observation_space_low, high=observation_space_high)

    @lru_cache(maxsize=None)
    def observation(self, observation: GridWorldState) -> np.ndarray:

        is_terminal_state = TerminalStateValidator.is_terminal_state(observation)

        if is_terminal_state:

            north_step = observation
            east_step = observation
            south_step = observation
            west_step = observation

        else:

            dynamics = GridWorldDynamics(observation)

            north_step = dynamics.step(GridWorldAction.NORTH)
            east_step = dynamics.step(GridWorldAction.EAST)
            south_step = dynamics.step(GridWorldAction.SOUTH)
            west_step = dynamics.step(GridWorldAction.WEST)

        north_step_distance_calculator = EuclideanDistanceCalculator(north_step)
        east_step_distance_calculator = EuclideanDistanceCalculator(east_step)
        south_step_distance_calculator = EuclideanDistanceCalculator(south_step)
        west_step_distance_calculator = EuclideanDistanceCalculator(west_step)

        return np.asarray([
            north_step_distance_calculator.distance_to_key(),
            east_step_distance_calculator.distance_to_key(),
            south_step_distance_calculator.distance_to_key(),
            west_step_distance_calculator.distance_to_key(),

            north_step_distance_calculator.distance_to_lock(),
            east_step_distance_calculator.distance_to_lock(),
            south_step_distance_calculator.distance_to_lock(),
            west_step_distance_calculator.distance_to_lock(),

            north_step_distance_calculator.distance_to_closest_beacon(),
            east_step_distance_calculator.distance_to_closest_beacon(),
            south_step_distance_calculator.distance_to_closest_beacon(),
            west_step_distance_calculator.distance_to_closest_beacon(),

            1 if north_step.is_in_pit() else 0,
            1 if east_step.is_in_pit() else 0,
            1 if south_step.is_in_pit() else 0,
            1 if west_step.is_in_pit() else 0,

            1 if observation.player_has_key() else 0
        ])
