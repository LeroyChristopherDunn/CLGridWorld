from unittest import TestCase

import numpy as np

from clgridworld.grid_world_grid_state import GridWorldGridState
from tests.grid_world_state_builder import GridWorldStateBuilder


class TestGridWorldGridState(TestCase):

    def test_state_size(self):

        shape = (20, 25)

        state = GridWorldStateBuilder.create_state_with_spec(shape=shape)
        grid_state = GridWorldGridState(state)

        self.assertEqual(shape, grid_state.grid.shape)

    def test_player_coords(self):

        player_coords = (2, 3)

        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)
        grid_state = GridWorldGridState(state)

        self.assertEqual(GridWorldGridState.PLAYER, grid_state.grid[player_coords])

        # alternative notations
        self.assertEqual(GridWorldGridState.PLAYER, grid_state.grid[player_coords[0], player_coords[1]])
        self.assertEqual(GridWorldGridState.PLAYER, grid_state.grid[player_coords[0]][player_coords[1]])

    def test_key_coords(self):

        key_coords = (5, 4)

        state = GridWorldStateBuilder.create_state_with_spec(key_coords=key_coords)
        grid_state = GridWorldGridState(state)

        self.assertEqual(GridWorldGridState.KEY, grid_state.grid[key_coords])

    def test_lock_coords(self):

        lock_coords = (5, 4)

        state = GridWorldStateBuilder.create_state_with_spec(lock_coords=lock_coords)
        grid_state = GridWorldGridState(state)

        self.assertEqual(GridWorldGridState.LOCK, grid_state.grid[lock_coords])

    def test_pit_coords(self):

        pit_start = (4, 2)
        pit_end = (4, 7)

        state = GridWorldStateBuilder.create_state_with_spec(pit_start_coords=pit_start, pit_end_coords=pit_end)
        grid_state = GridWorldGridState(state)

        pit_state = grid_state.grid[pit_start[0]:pit_end[0]+1, pit_start[1]:pit_end[1]+1]

        self.assertTrue(np.all(pit_state == GridWorldGridState.PIT))
