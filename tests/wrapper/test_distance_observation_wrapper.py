from unittest import TestCase

import numpy as np

from clgridworld.action.action import GridWorldAction
from clgridworld.grid_world_builder import InitialStateParams, GridWorldBuilder
from clgridworld.wrapper.distance_observation_wrapper import DistanceObservationWrapper


class TestDistanceObservationWrapper(TestCase):

    def test_target_task_initial_state(self):

        params = InitialStateParams(shape=(10, 10), player=(1, 4), key=(7, 5), lock=(1, 1), pit_start=(4, 2),
                                    pit_end=(4, 7))
        env = GridWorldBuilder.create(params)

        env_wrapper = DistanceObservationWrapper(env)

        state = env_wrapper.reset()

        # north, east, south, west
        expected_state = [7.07, 6, 5.10, 6.32, 3.16, 4, 3.16, 2, 4.24, 3.61, 3.16, 2.83, 0, 0, 0, 0, 0]

        np.testing.assert_almost_equal(expected_state, state, 2)

    def test_terminal_state(self):

        params = InitialStateParams(shape=(10, 10), player=(3, 4), key=(7, 5), lock=(1, 1), pit_start=(4, 2),
                                    pit_end=(4, 7))
        env = GridWorldBuilder.create(params)
        env_wrapper = DistanceObservationWrapper(env)

        state = env_wrapper.step(GridWorldAction.SOUTH)
