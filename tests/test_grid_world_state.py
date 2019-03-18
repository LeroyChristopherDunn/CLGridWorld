from unittest import TestCase

from clgridworld.grid_world_state import GridWorldStateFactory, GridWorldStateKey
from tests.grid_world_state_builder import GridWorldStateBuilder


class TestGridWorldState(TestCase):

    def test_given_valid_parameters_should_correctly_create_state(self):

        #  target task spec in 'Autonomous Task Sequencing... Narvekar et al 2017'
        shape = (10, 10)
        player_coords = (1, 4)
        key_coords = (7, 5)
        lock_coords = (1, 1)
        pit_start_coords = (4, 2)
        pit_end_coords = (4, 7)

        nw_beacon = (3, 1)
        ne_beacon = (3, 8)
        sw_beacon = (5, 1)
        se_beacon = (5, 8)
        has_key = 0

        state = GridWorldStateFactory.create(shape, player_coords, key_coords, lock_coords, pit_start_coords,
                                             pit_end_coords)

        self.assertEqual(shape, state[GridWorldStateKey.GRID_SHAPE], "shape not equal")
        self.assertEqual(player_coords, state[GridWorldStateKey.PLAYER], "player coords not equal")
        self.assertEqual(key_coords, state[GridWorldStateKey.KEY], "key coords not equal")
        self.assertEqual(lock_coords, state[GridWorldStateKey.LOCK], "lock coords not equal")
        self.assertEqual(pit_start_coords, state[GridWorldStateKey.PIT_START], "pit start key not equal")
        self.assertEqual(pit_end_coords, state[GridWorldStateKey.PIT_END], "pit end key not equal")
        self.assertEqual(nw_beacon, state[GridWorldStateKey.NW_BEACON], "nw beacon coords not equal")
        self.assertEqual(ne_beacon, state[GridWorldStateKey.NE_BEACON], "ne beacon coords not equal")
        self.assertEqual(sw_beacon, state[GridWorldStateKey.SW_BEACON], "sw beacon coords not equal")
        self.assertEqual(se_beacon, state[GridWorldStateKey.SE_BEACON], "se beacon coords not equal")
        self.assertEqual(has_key, state[GridWorldStateKey.HAS_KEY], "has key not equal")

    def test_given_player_coords_out_of_bounds_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          player_coords=(-1, 0))
        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          player_coords=(9, 10), shape=(10, 10))

    def test_given_key_coords_out_of_bounds_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec, key_coords=(0, -1))
        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec, key_coords=(10, 9), shape=(10, 10))

    def test_given_lock_coords_out_of_bounds_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec, lock_coords=(0, -1))
        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec, lock_coords=(10, 9), shape=(10, 10))

    def test_given_pit_coords_out_of_bounds_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          pit_start_coords=(-1, 2), pit_end_coords=(4, 7), shape=(10, 10))
        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          pit_start_coords=(4, 2), pit_end_coords=(4, 10), shape=(10, 10))

    def test_given_player_coords_overlap_with_key_coords_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          player_coords=(0, 0), key_coords=(0, 0))

    def test_given_player_coords_overlap_with_lock_coords_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          player_coords=(1, 1), lock_coords=(1, 1))

    def test_given_key_coords_overlap_with_lock_coords_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          key_coords=(7, 5), lock_coords=(7, 5))

    def test_given_player_coords_overlap_with_pit_coords_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          player_coords=(4, 2), pit_start_coords=(4, 2), pit_end_coords=(4, 7))

    def test_given_lock_coords_overlap_with_pit_coords_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          lock_coords=(5, 3), pit_start_coords=(4, 2), pit_end_coords=(5, 7))

    def test_given_key_coords_overlap_with_pit_coords_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          key_coords=(5, 7), pit_start_coords=(4, 2), pit_end_coords=(5, 7))

    def test_given_player_coords_overlap_with_beacon_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          player_coords=(3, 1), pit_start_coords=(4, 2), pit_end_coords=(5, 7))

    def test_given_key_coords_overlap_with_beacon_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          key_coords=(6, 8), pit_start_coords=(4, 2), pit_end_coords=(5, 7))

    def test_given_lock_coords_overlap_with_beacon_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          lock_coords=(6, 1), pit_start_coords=(4, 2), pit_end_coords=(5, 7))

    def test_given_pit_on_sw_bound_should_correctly_create_state(self):

        shape = (20, 20)
        pit_start_coords = (17, 0)
        pit_end_coords = (19, 3)

        ne_beacon = (16, 4)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)

        self.assertEqual(None, state[GridWorldStateKey.NW_BEACON], "nw beacon coords not equal")
        self.assertEqual(ne_beacon, state[GridWorldStateKey.NE_BEACON], "ne beacon coords not equal")
        self.assertEqual(None, state[GridWorldStateKey.SW_BEACON], "sw beacon coords not equal")
        self.assertEqual(None, state[GridWorldStateKey.SE_BEACON], "se beacon coords not equal")

    def test_given_pit_on_south_bound_should_correctly_create_state(self):

        shape = (20, 20)
        pit_start_coords = (17, 3)
        pit_end_coords = (19, 6)

        nw_beacon = (16, 2)
        ne_beacon = (16, 7)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)

        self.assertEqual(nw_beacon, state[GridWorldStateKey.NW_BEACON], "nw beacon coords not equal")
        self.assertEqual(ne_beacon, state[GridWorldStateKey.NE_BEACON], "ne beacon coords not equal")
        self.assertEqual(None, state[GridWorldStateKey.SW_BEACON], "sw beacon coords not equal")
        self.assertEqual(None, state[GridWorldStateKey.SE_BEACON], "se beacon coords not equal")

    def test_given_pit_on_ne_bound_should_correctly_create_state(self):

        shape = (20, 20)
        pit_start_coords = (0, 17)
        pit_end_coords = (3, 19)

        sw_beacon = (4, 16)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)

        self.assertEqual(None, state[GridWorldStateKey.NW_BEACON], "nw beacon coords not equal")
        self.assertEqual(None, state[GridWorldStateKey.NE_BEACON], "ne beacon coords not equal")
        self.assertEqual(sw_beacon, state[GridWorldStateKey.SW_BEACON], "sw beacon coords not equal")
        self.assertEqual(None, state[GridWorldStateKey.SE_BEACON], "se beacon coords not equal")

    def test_given_no_pit_should_correctly_create_state(self):

        #  target task spec in 'Autonomous Task Sequencing... Narvekar et al 2017'
        shape = (10, 10)
        player_coords = (1, 4)
        key_coords = (7, 5)
        lock_coords = (1, 1)
        pit_start_coords = None
        pit_end_coords = None

        nw_beacon = None
        ne_beacon = None
        sw_beacon = None
        se_beacon = None

        state = GridWorldStateFactory.create(shape, player_coords, key_coords, lock_coords, pit_start_coords, pit_end_coords)

        self.assertEqual(shape, state[GridWorldStateKey.GRID_SHAPE], "shape not equal")
        self.assertEqual(player_coords, state[GridWorldStateKey.PLAYER], "player coords not equal")
        self.assertEqual(key_coords, state[GridWorldStateKey.KEY], "key coords not equal")
        self.assertEqual(lock_coords, state[GridWorldStateKey.LOCK], "lock coords not equal")
        self.assertEqual(pit_start_coords, state[GridWorldStateKey.PIT_START], "pit start key not equal")
        self.assertEqual(pit_end_coords, state[GridWorldStateKey.PIT_END], "pit end key not equal")
        self.assertEqual(nw_beacon, state[GridWorldStateKey.NW_BEACON], "nw beacon coords not equal")
        self.assertEqual(ne_beacon, state[GridWorldStateKey.NE_BEACON], "ne beacon coords not equal")
        self.assertEqual(sw_beacon, state[GridWorldStateKey.SW_BEACON], "sw beacon coords not equal")
        self.assertEqual(se_beacon, state[GridWorldStateKey.SE_BEACON], "se beacon coords not equal")
        self.assertEqual(0, state[GridWorldStateKey.HAS_KEY], "has key not equal")

    def test_given_single_set_of_pit_coords_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          pit_start_coords=None, pit_end_coords=(4, 7))
        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          pit_start_coords=(4, 7), pit_end_coords=None)

    def test_given_no_key_should_correctly_create_state(self):

        key_coords = None

        has_key = 1

        state = GridWorldStateBuilder.create_state_with_spec(key_coords=key_coords)

        self.assertEqual(key_coords, state[GridWorldStateKey.KEY], "key coords not equal")
        self.assertEqual(has_key, state[GridWorldStateKey.HAS_KEY], "has key not equal")

    def test_given_no_lock_should_correctly_create_state(self):

        lock_coords = None

        state = GridWorldStateBuilder.create_state_with_spec(lock_coords=lock_coords)

        self.assertEqual(lock_coords, state[GridWorldStateKey.LOCK], "lock coords not equal")

    def test_given_no_key_and_lock_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          key_coords=None, lock_coords=None)

