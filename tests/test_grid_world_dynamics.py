from unittest import TestCase

from clgridworld.grid_world_actions import GridWorldActions
from clgridworld.grid_world_dynamics import GridWorldDynamics
from clgridworld.grid_world_state import GridWorldState
from tests.grid_world_state_builder import GridWorldStateBuilder


class TestGridWorldDynamics(TestCase):

    def test_new_state_should_be_new_object(self):

        player_coords = (0, 0)
        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.NORTH)

        self.assertFalse(state is new_state)

    def test_when_player_moves_into_top_boundary_should_remain_in_same_state(self):

        player_coords = (0, 0)
        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.NORTH)

        self.assertEqual(state, new_state)

    def test_when_player_moves_into_left_boundary_should_remain_in_same_state(self):

        player_coords = (0, 0)
        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.WEST)

        self.assertEqual(state, new_state)

    def test_when_player_moves_into_bottom_boundary_should_remain_in_same_state(self):

        player_coords = (9, 9)
        state = GridWorldStateBuilder.create_state_with_spec(shape=(10, 10), player_coords=player_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.SOUTH)

        self.assertEqual(state, new_state)

    def test_when_player_moves_into_right_boundary_should_remain_in_same_state(self):

        player_coords = (9, 9)
        state = GridWorldStateBuilder.create_state_with_spec(shape=(10, 10), player_coords=player_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.EAST)

        self.assertEqual(state, new_state)

    def test_when_player_moves_north_into_empty_space_should_move_to_empty_space(self):

        player_coords = (1, 0)
        expected_player_state = (0, 0)

        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)
        actual_state = GridWorldDynamics(state).step(GridWorldActions.NORTH)

        expected_state = state.copy()
        expected_state[GridWorldState.PLAYER_KEY] = expected_player_state
        self.assertEqual(expected_state, actual_state)

    def test_when_player_moves_east_into_empty_space_should_move_to_empty_space(self):

        player_coords = (0, 0)
        expected_player_state = (0, 1)

        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)
        actual_state = GridWorldDynamics(state).step(GridWorldActions.EAST)

        expected_state = state.copy()
        expected_state[GridWorldState.PLAYER_KEY] = expected_player_state
        self.assertEqual(expected_state, actual_state)

    def test_when_player_moves_south_into_empty_space_should_move_to_empty_space(self):

        player_coords = (0, 0)
        expected_player_state = (1, 0)

        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)
        actual_state = GridWorldDynamics(state).step(GridWorldActions.SOUTH)

        expected_state = state.copy()
        expected_state[GridWorldState.PLAYER_KEY] = expected_player_state
        self.assertEqual(expected_state, actual_state)

    def test_when_player_moves_west_into_empty_space_should_move_to_empty_space(self):

        player_coords = (0, 1)
        expected_player_state = (0, 0)

        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)
        actual_state = GridWorldDynamics(state).step(GridWorldActions.WEST)

        expected_state = state.copy()
        expected_state[GridWorldState.PLAYER_KEY] = expected_player_state
        self.assertEqual(expected_state, actual_state)

    def test_when_player_moves_north_into_beacon_should_remain_in_same_state(self):

        shape = (10, 10)
        player_coords = (6, 1)
        pit_start_coords = (4, 2)
        pit_end_coords = (4, 7)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, player_coords=player_coords, pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.NORTH)

        self.assertEqual(state, new_state)

    def test_when_player_moves_east_into_beacon_should_remain_in_same_state(self):

        shape = (10, 10)
        player_coords = (5, 0)
        pit_start_coords = (4, 2)
        pit_end_coords = (4, 7)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, player_coords=player_coords, pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.EAST)

        self.assertEqual(state, new_state)

    def test_when_player_moves_west_into_beacon_should_remain_in_same_state(self):

        shape = (10, 10)
        player_coords = (3, 9)
        pit_start_coords = (4, 2)
        pit_end_coords = (4, 7)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, player_coords=player_coords, pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.WEST)

        self.assertEqual(state, new_state)

    def test_when_player_moves_south_into_beacon_should_remain_in_same_state(self):

        shape = (10, 10)
        player_coords = (2, 8)
        pit_start_coords = (4, 2)
        pit_end_coords = (4, 7)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, player_coords=player_coords, pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.SOUTH)

        self.assertEqual(state, new_state)
