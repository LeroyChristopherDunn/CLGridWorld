from clgridworld.state.state import GridWorldState
from clgridworld.state.state_factory import GridWorldStateFactory


class GridWorldStateBuilder:

    @staticmethod
    def create_state_with_spec(shape=(10, 10), player_coords=(1, 4), key_coords=(7, 5), lock_coords=(1, 1),
                               pit_start_coords=(4, 2), pit_end_coords=(4, 7)) -> GridWorldState:

        #  defaults to target task spec in 'Autonomous Task Sequencing... Narvekar et al 2017'
        return GridWorldStateFactory.create(shape, player_coords, key_coords, lock_coords, pit_start_coords,
                                            pit_end_coords)
