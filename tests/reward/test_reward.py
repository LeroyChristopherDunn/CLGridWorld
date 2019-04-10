from unittest import TestCase

from clgridworld.action.action import GridWorldAction
from clgridworld.dynamics.dynamics import GridWorldDynamics
from clgridworld.reward.reward import GridWorldRewardFunction, GridWorldReward
from tests.state.grid_world_state_builder import GridWorldStateBuilder


class GridWorldRewardTest(TestCase):

    def setUp(self):
        super().setUp()
        self.expected_reward = GridWorldReward()

    def test_given_same_state_should_return_correct_reward(self):

        curr_state = GridWorldStateBuilder.create_state_with_spec()
        next_state = GridWorldStateBuilder.create_state_with_spec()

        reward = GridWorldRewardFunction().calculate(curr_state, next_state)

        self.assertEqual(self.expected_reward.no_movement, reward)

    def test_given_player_moved_into_empty_space_should_return_correct_reward(self):

        player_coords = (0, 0)

        curr_state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)
        next_state = GridWorldDynamics(curr_state).step(GridWorldAction.EAST)

        reward = GridWorldRewardFunction().calculate(curr_state, next_state)

        self.assertFalse(curr_state == next_state, "states should not be equal")
        self.assertEqual(self.expected_reward.player_moved_into_empty_space, reward)

    def test_given_player_picked_up_key_should_return_correct_reward(self):

        player_coords = (0, 0)
        key_coords = (1, 0)

        curr_state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords, key_coords=key_coords)
        next_state = GridWorldDynamics(curr_state).step(GridWorldAction.PICK_UP_KEY)

        reward = GridWorldRewardFunction().calculate(curr_state, next_state)

        self.assertEqual(self.expected_reward.player_picked_up_key, reward)

    def test_given_player_unlocked_lock_should_return_correct_reward(self):

        player_coords = (0, 0)
        key_coords = None
        lock_coords = (1, 0)

        curr_state = GridWorldStateBuilder.create_state_with_spec(
            player_coords=player_coords, key_coords=key_coords, lock_coords=lock_coords)
        next_state = GridWorldDynamics(curr_state).step(GridWorldAction.UNLOCK_LOCK)

        reward = GridWorldRewardFunction().calculate(curr_state, next_state)

        self.assertEqual(self.expected_reward.player_unlocked_lock, reward)

    def test_given_player_moved_into_pit_should_return_correct_reward(self):

        shape = (10, 10)
        pit_start_coords = (4, 2)
        pit_end_coords = (4, 7)
        player_coords = (5, 4)

        curr_state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, player_coords=player_coords, pit_start_coords=pit_start_coords,
            pit_end_coords=pit_end_coords)
        next_state = GridWorldDynamics(curr_state).step(GridWorldAction.NORTH)

        reward = GridWorldRewardFunction().calculate(curr_state, next_state)

        self.assertEqual(self.expected_reward.player_moved_into_pit, reward)
