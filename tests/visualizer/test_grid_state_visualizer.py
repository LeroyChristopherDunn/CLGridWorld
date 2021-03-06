from unittest import TestCase

import numpy as np

from clgridworld.visualizer.grid_state_visualizer import GridStateVisualizer
from tests.state.grid_world_state_builder import GridWorldStateBuilder


class TestGridWorldGridState(TestCase):

    def test_state_size(self):

        shape = (20, 25)

        state = GridWorldStateBuilder.create_state_with_spec(shape=shape)
        grid = GridStateVisualizer(state).grid

        self.assertEqual(shape, grid.shape)

    def test_player_coords(self):

        player_coords = (2, 3)

        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)
        grid = GridStateVisualizer(state).grid

        self.assertEqual(GridStateVisualizer.PLAYER, grid[player_coords])

        # alternative notations
        self.assertEqual(GridStateVisualizer.PLAYER, grid[player_coords[0], player_coords[1]])
        self.assertEqual(GridStateVisualizer.PLAYER, grid[player_coords[0]][player_coords[1]])

    def test_key_coords(self):

        key_coords = (5, 4)

        state = GridWorldStateBuilder.create_state_with_spec(key_coords=key_coords)
        grid = GridStateVisualizer(state).grid

        self.assertEqual(GridStateVisualizer.KEY, grid[key_coords])

    def test_lock_coords(self):

        lock_coords = (5, 4)

        state = GridWorldStateBuilder.create_state_with_spec(lock_coords=lock_coords)
        grid = GridStateVisualizer(state).grid

        self.assertEqual(GridStateVisualizer.LOCK, grid[lock_coords])

    def test_pit_coords(self):

        pit_start = (4, 2)
        pit_end = (4, 7)

        state = GridWorldStateBuilder.create_state_with_spec(pit_start_coords=pit_start, pit_end_coords=pit_end)
        grid = GridStateVisualizer(state).grid

        pit_state = grid[pit_start[0]:pit_end[0]+1, pit_start[1]:pit_end[1]+1]

        self.assertTrue(np.all(pit_state == GridStateVisualizer.PIT))

    def test_no_key_coords(self):

        key_coords = None

        state = GridWorldStateBuilder.create_state_with_spec(key_coords=key_coords)
        grid = GridStateVisualizer(state).grid

        self.assertFalse(np.any(grid == GridStateVisualizer.KEY), "key should not be on grid")
        
    def test_no_lock_coords(self):

        lock_coords = None

        state = GridWorldStateBuilder.create_state_with_spec(lock_coords=lock_coords)
        grid = GridStateVisualizer(state).grid

        self.assertFalse(np.any(grid == GridStateVisualizer.LOCK), "lock should not be on grid")

    def test_no_pit_coords(self):

        pit_start_coords = None
        pit_end_coords = None

        state = GridWorldStateBuilder.create_state_with_spec(
            pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)
        grid = GridStateVisualizer(state).grid

        self.assertFalse(np.any(grid == GridStateVisualizer.PIT), "pit should not be on grid")

    def test_beacons_for_pit_in_bound(self):

        # target task desc in Auto Sequencing..., Narverkar 2017

        pit_start = (4, 2)
        pit_end = (4, 7)

        state = GridWorldStateBuilder.create_state_with_spec(pit_start_coords=pit_start, pit_end_coords=pit_end)
        grid = GridStateVisualizer(state).grid

        self.assertEqual(GridStateVisualizer.BEACON, grid[3, 1])  # top left
        self.assertEqual(GridStateVisualizer.BEACON, grid[3, 8])  # bottom left
        self.assertEqual(GridStateVisualizer.BEACON, grid[5, 1])  # top right
        self.assertEqual(GridStateVisualizer.BEACON, grid[5, 8])  # bottom right

    def test_beacon_for_pit_on_bottom_left_state_bound(self):

        shape = (10, 10)
        pit_start = (7, 0)
        pit_end = (9, 3)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, pit_start_coords=pit_start, pit_end_coords=pit_end)
        grid = GridStateVisualizer(state).grid

        self.assertEqual(GridStateVisualizer.BEACON, grid[6, 4])  # top right

        grid[6, 4] = GridStateVisualizer.EMPTY
        self.assertFalse(np.any(grid == GridStateVisualizer.BEACON), "additional beacons should not be on grid")

    def test_beacons_for_pit_on_bottom_state_bound(self):

        shape = (10, 10)
        pit_start = (7, 3)
        pit_end = (9, 5)
        key_coords = (1, 2)

        state = GridWorldStateBuilder.create_state_with_spec(
            key_coords=key_coords, shape=shape, pit_start_coords=pit_start, pit_end_coords=pit_end)
        grid = GridStateVisualizer(state).grid

        self.assertEqual(GridStateVisualizer.BEACON, grid[6, 2])  # top left
        self.assertEqual(GridStateVisualizer.BEACON, grid[6, 6])  # top right

        grid[6, 2] = GridStateVisualizer.EMPTY
        grid[6, 6] = GridStateVisualizer.EMPTY
        self.assertFalse(np.any(grid == GridStateVisualizer.BEACON), "additional beacons should not be on grid")

    def test_beacons_for_pit_on_top_right_state_bound(self):

        shape = (10, 10)
        pit_start = (0, 7)
        pit_end = (3, 9)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, pit_start_coords=pit_start, pit_end_coords=pit_end)
        grid = GridStateVisualizer(state).grid

        self.assertEqual(GridStateVisualizer.BEACON, grid[4, 6])  # bottom left

        grid[4, 6] = GridStateVisualizer.EMPTY
        self.assertFalse(np.any(grid == GridStateVisualizer.BEACON), "additional beacons should not be on grid")
