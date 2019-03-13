from unittest import TestCase

from clgridworld.grid_world_state import GridWorldState


class TestGridWorldState(TestCase):

    @staticmethod
    def create_state_with_spec(shape=(10, 10), player_coords=(1, 4), key_coords=(7, 5), lock_coords=(1, 1), pit_coords=((4, 2), (5, 8))):

        #  defaults to target task spec in 'Autonomous Task Sequencing... Narvekar et al 2017'
        return GridWorldState.create(shape, player_coords, key_coords, lock_coords, pit_coords)

    def test_given_valid_parameters_should_correctly_create_state(self):

        #  target task spec in 'Autonomous Task Sequencing... Narvekar et al 2017'
        shape = (10, 10)
        player_coords = (1, 4)
        key_coords = (7, 5)
        lock_coords = (1, 1)
        pit_coords = ((4, 2), (5, 8))

        nw_beacon = (3, 1)
        ne_beacon = (3, 8)
        sw_beacon = (5, 1)
        se_beacon = (5, 8)

        state = GridWorldState.create(shape, player_coords, key_coords, lock_coords, pit_coords)

        self.assertEqual(shape, state[GridWorldState.GRID_SHAPE_KEY], "shape not equal")
        self.assertEqual(player_coords, state[GridWorldState.PLAYER_KEY], "player coords not equal")
        self.assertEqual(key_coords, state[GridWorldState.KEY_DICT_KEY], "key coords not equal")
        self.assertEqual(lock_coords, state[GridWorldState.LOCK_KEY], "lock coords not equal")
        self.assertEqual(pit_coords, state[GridWorldState.PIT_KEY], "pit coords not equal")
        self.assertEqual(nw_beacon, state[GridWorldState.NW_BEACON_KEY], "nw beacon coords not equal")
        self.assertEqual(ne_beacon, state[GridWorldState.NE_BEACON_KEY], "ne beacon coords not equal")
        self.assertEqual(sw_beacon, state[GridWorldState.SW_BEACON_KEY], "sw beacon coords not equal")
        self.assertEqual(se_beacon, state[GridWorldState.SE_BEACON_KEY], "se beacon coords not equal")
        self.assertEqual(0, state[GridWorldState.HAS_KEY_DICT_KEY], "has key not equal")

    def test_given_player_coords_out_of_bounds_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, player_coords=(-1, 0))
        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, player_coords=(9, 10), shape=(10, 10))

    def test_given_key_coords_out_of_bounds_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, key_coords=(0, -1))
        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, key_coords=(10, 9), shape=(10, 10))

    def test_given_lock_coords_out_of_bounds_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, lock_coords=(0, -1))
        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, lock_coords=(10, 9), shape=(10, 10))

    def test_given_pit_coords_out_of_bounds_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, pit_coords=((-1, 2), (5, 8)), shape=(10, 10))
        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, pit_coords=((4, 2), (5, 10)), shape=(10, 10))

    def test_given_player_coords_overlap_with_key_coords_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, player_coords=(0, 0), key_coords=(0, 0))

    def test_given_player_coords_overlap_with_lock_coords_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, player_coords=(1, 1), lock_coords=(1, 1))

    def test_given_key_coords_overlap_with_lock_coords_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, key_coords=(7, 5), lock_coords=(7, 5))

    def test_given_player_coords_overlap_with_pit_coords_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, player_coords=(4, 2), pit_coords=((4, 2), (5, 8)))

    def test_given_lock_coords_overlap_with_pit_coords_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, lock_coords=(5, 3), pit_coords=((4, 2), (6, 8)))

    def test_given_key_coords_overlap_with_pit_coords_should_throw_error(self):

        self.assertRaises(ValueError, TestGridWorldState.create_state_with_spec, key_coords=(5, 7), pit_coords=((4, 2), (6, 8)))


