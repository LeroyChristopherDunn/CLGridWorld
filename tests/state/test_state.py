from unittest import TestCase

from clgridworld.state.state_factory import GridWorldStateFactory
from tests.state.grid_world_state_builder import GridWorldStateBuilder


class TestGridWorldStateFactory(TestCase):

    def test_hash(self):

        shape = (10, 10)
        player_coords = (1, 4)
        key_coords = (7, 5)

        state1 = GridWorldStateFactory.create(shape, player_coords, key_coords)
        state2 = GridWorldStateFactory.create(shape, player_coords, key_coords)
        state3 = GridWorldStateFactory.create(shape, (9, 9), key_coords)

        self.assertEqual(state1.__hash__(), state2.__hash__())
        self.assertNotEqual(state1.__hash__(), state3.__hash__())

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

        self.assertEqual(shape, state.grid_shape, "shape not equal")
        self.assertEqual(player_coords, state.player, "player coords not equal")
        self.assertEqual(key_coords, state.key, "key coords not equal")
        self.assertEqual(lock_coords, state.lock, "lock coords not equal")
        self.assertEqual(pit_start_coords, state.pit_start, "pit start key not equal")
        self.assertEqual(pit_end_coords, state.pit_end, "pit end key not equal")
        self.assertEqual(nw_beacon, state.nw_beacon, "nw beacon coords not equal")
        self.assertEqual(ne_beacon, state.ne_beacon, "ne beacon coords not equal")
        self.assertEqual(sw_beacon, state.sw_beacon, "sw beacon coords not equal")
        self.assertEqual(se_beacon, state.se_beacon, "se beacon coords not equal")
        self.assertEqual(has_key, state.has_key, "has key not equal")

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

        self.assertEqual(None, state.nw_beacon, "nw beacon coords not equal")
        self.assertEqual(ne_beacon, state.ne_beacon, "ne beacon coords not equal")
        self.assertEqual(None, state.sw_beacon, "sw beacon coords not equal")
        self.assertEqual(None, state.se_beacon, "se beacon coords not equal")

    def test_given_pit_on_south_bound_should_correctly_create_state(self):

        shape = (20, 20)
        pit_start_coords = (17, 3)
        pit_end_coords = (19, 6)

        nw_beacon = (16, 2)
        ne_beacon = (16, 7)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)

        self.assertEqual(nw_beacon, state.nw_beacon, "nw beacon coords not equal")
        self.assertEqual(ne_beacon, state.ne_beacon, "ne beacon coords not equal")
        self.assertEqual(None, state.sw_beacon, "sw beacon coords not equal")
        self.assertEqual(None, state.se_beacon, "se beacon coords not equal")

    def test_given_pit_on_ne_bound_should_correctly_create_state(self):

        shape = (20, 20)
        pit_start_coords = (0, 17)
        pit_end_coords = (3, 19)

        sw_beacon = (4, 16)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, pit_start_coords=pit_start_coords, pit_end_coords=pit_end_coords)

        self.assertEqual(None, state.nw_beacon, "nw beacon coords not equal")
        self.assertEqual(None, state.ne_beacon, "ne beacon coords not equal")
        self.assertEqual(sw_beacon, state.sw_beacon, "sw beacon coords not equal")
        self.assertEqual(None, state.se_beacon, "se beacon coords not equal")

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

        self.assertEqual(shape, state.grid_shape, "shape not equal")
        self.assertEqual(player_coords, state.player, "player coords not equal")
        self.assertEqual(key_coords, state.key, "key coords not equal")
        self.assertEqual(lock_coords, state.lock, "lock coords not equal")
        self.assertEqual(pit_start_coords, state.pit_start, "pit start key not equal")
        self.assertEqual(pit_end_coords, state.pit_end, "pit end key not equal")
        self.assertEqual(nw_beacon, state.nw_beacon, "nw beacon coords not equal")
        self.assertEqual(ne_beacon, state.ne_beacon, "ne beacon coords not equal")
        self.assertEqual(sw_beacon, state.sw_beacon, "sw beacon coords not equal")
        self.assertEqual(se_beacon, state.se_beacon, "se beacon coords not equal")
        self.assertEqual(False, state.has_key, "has key not equal")

    def test_given_single_set_of_pit_coords_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          pit_start_coords=None, pit_end_coords=(4, 7))
        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          pit_start_coords=(4, 7), pit_end_coords=None)

    def test_given_no_key_should_correctly_create_state(self):

        key_coords = None

        has_key = 1

        state = GridWorldStateBuilder.create_state_with_spec(key_coords=key_coords)

        self.assertEqual(key_coords, state.key, "key coords not equal")
        self.assertEqual(has_key, state.has_key, "has key not equal")

    def test_given_no_lock_should_correctly_create_state(self):

        lock_coords = None

        state = GridWorldStateBuilder.create_state_with_spec(lock_coords=lock_coords)

        self.assertEqual(lock_coords, state.lock, "lock coords not equal")

    def test_given_no_key_and_lock_should_throw_error(self):

        self.assertRaises(ValueError, GridWorldStateBuilder.create_state_with_spec,
                          key_coords=None, lock_coords=None)

    def test_given_no_key_and_no_pit_should_not_throw_error(self):
        
        shape = (10, 10)
        player_coords = (1, 4)
        key_coords = None
        pit_start_coords = None
        pit_end_coords = None

        state = GridWorldStateBuilder.create_state_with_spec(shape=shape, player_coords=player_coords, 
                                                             key_coords=key_coords, pit_start_coords=pit_start_coords, 
                                                             pit_end_coords=pit_end_coords)

        self.assertEqual(shape, state.grid_shape, "shape not equal")
        self.assertEqual(player_coords, state.player, "player coords not equal")
        self.assertEqual(key_coords, state.key, "key coords not equal")
        self.assertEqual(pit_start_coords, state.pit_start, "pit start key not equal")
        self.assertEqual(pit_end_coords, state.pit_end, "pit end key not equal")

    def test_given_no_lock_and_no_pit_should_not_throw_error(self):
        
        shape = (10, 10)
        player_coords = (1, 4)
        lock_coords = None
        pit_start_coords = None
        pit_end_coords = None

        state = GridWorldStateBuilder.create_state_with_spec(shape=shape, player_coords=player_coords,
                                                             lock_coords=lock_coords, pit_start_coords=pit_start_coords,
                                                             pit_end_coords=pit_end_coords)

        self.assertEqual(shape, state.grid_shape, "shape not equal")
        self.assertEqual(player_coords, state.player, "player coords not equal")
        self.assertEqual(lock_coords, state.lock, "lock coords not equal")
        self.assertEqual(pit_start_coords, state.pit_start, "pit start lock not equal")
        self.assertEqual(pit_end_coords, state.pit_end, "pit end lock not equal")
