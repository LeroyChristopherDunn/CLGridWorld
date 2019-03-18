from clgridworld.grid_world_actions import GridWorldActions
from clgridworld.grid_world_state import GridWorldState


class GridWorldDynamics:

    def __init__(self, state):
        self.state = state

        self.beacons = [state[GridWorldState.NW_BEACON_KEY], state[GridWorldState.NE_BEACON_KEY],
                        state[GridWorldState.SW_BEACON_KEY], state[GridWorldState.SE_BEACON_KEY]].copy()

    def step(self, action) -> dict:  # this should return a state

        if self._player_moves_into_boundary(action):
            return self.state.copy()

        if self._player_moves_into_beacon(action):
            return self.state.copy()

        return self._translate_player(action)

    def _translate_player(self, action):

        player_coords = self.state[GridWorldState.PLAYER_KEY]
        new_player_coords = GridWorldDynamics._translate_coords(player_coords, action)
        new_state = self.state.copy()
        new_state[GridWorldState.PLAYER_KEY] = new_player_coords
        return new_state

    def _player_moves_into_boundary(self, action):

        player_coords = self.state[GridWorldState.PLAYER_KEY]
        shape = self.state[GridWorldState.GRID_SHAPE_KEY]

        if action == GridWorldActions.NORTH:
            return player_coords[0] == 0

        elif action == GridWorldActions.EAST:
            return player_coords[1] == shape[0] - 1

        elif action == GridWorldActions.SOUTH:
            return player_coords[0] == shape[1] - 1

        elif action == GridWorldActions.WEST:
            return player_coords[1] == 0

    def _player_moves_into_beacon(self, action):

        player_coords = self.state[GridWorldState.PLAYER_KEY]
        new_player_coords = GridWorldDynamics._translate_coords(player_coords, action)

        return new_player_coords in self.beacons

    @staticmethod
    def _translate_coords(coords: (int, int), action):

        new_coords = tuple(coords)

        if action == GridWorldActions.NORTH:
            new_coords = (coords[0] - 1, coords[1])

        elif action == GridWorldActions.EAST:
            new_coords = (coords[0], coords[1] + 1)

        elif action == GridWorldActions.SOUTH:
            new_coords = (coords[0] + 1, coords[1])

        elif action == GridWorldActions.WEST:
            new_coords = (coords[0], coords[1] - 1)

        return new_coords


