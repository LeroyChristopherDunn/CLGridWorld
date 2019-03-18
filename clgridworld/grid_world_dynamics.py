from clgridworld.grid_world_actions import GridWorldActions as ACTIONS
from clgridworld.grid_world_state import GridWorldStateKey as STATE, GridWorldState


class GridWorldDynamics:

    def __init__(self, state: GridWorldState):

        self.state = state
        self._immovable_objects = [state[STATE.KEY_DICT_KEY], state[STATE.LOCK_KEY],
                                   state[STATE.NW_BEACON_KEY], state[STATE.NE_BEACON_KEY],
                                   state[STATE.SW_BEACON_KEY], state[STATE.SE_BEACON_KEY]].copy()

    def step(self, action) -> GridWorldState:

        if self._player_moves_into_boundary(action):
            return self.state.copy()

        if self._player_moves_into_immovable_object(action):
            return self.state.copy()

        if self._player_picks_up_key_from_eligible_coords(action):
            return self._pick_up_key()

        return GridWorldState(self._translate_player(action))

    def _translate_player(self, action) -> GridWorldState:

        player_coords = self.state[STATE.PLAYER_KEY]
        new_player_coords = GridWorldDynamics._translate_coords(player_coords, action)
        new_state = self.state.copy()
        new_state[STATE.PLAYER_KEY] = new_player_coords
        return GridWorldState(new_state)

    def _player_moves_into_boundary(self, action) -> bool:

        player_coords = self.state[STATE.PLAYER_KEY]
        shape = self.state[STATE.GRID_SHAPE_KEY]

        if action == ACTIONS.NORTH:
            return player_coords[0] == 0

        elif action == ACTIONS.EAST:
            return player_coords[1] == shape[0] - 1

        elif action == ACTIONS.SOUTH:
            return player_coords[0] == shape[1] - 1

        elif action == ACTIONS.WEST:
            return player_coords[1] == 0

    def _player_moves_into_immovable_object(self, action) -> bool:

        player_coords = self.state[STATE.PLAYER_KEY]
        new_player_coords = GridWorldDynamics._translate_coords(player_coords, action)

        return new_player_coords in self._immovable_objects

    @staticmethod
    def _translate_coords(coords: (int, int), action) -> (int, int):

        new_coords = tuple(coords)

        if action == ACTIONS.NORTH:
            new_coords = (coords[0] - 1, coords[1])

        elif action == ACTIONS.EAST:
            new_coords = (coords[0], coords[1] + 1)

        elif action == ACTIONS.SOUTH:
            new_coords = (coords[0] + 1, coords[1])

        elif action == ACTIONS.WEST:
            new_coords = (coords[0], coords[1] - 1)

        return new_coords

    def _player_picks_up_key_from_eligible_coords(self, action):

        if action is not ACTIONS.PICK_UP_KEY:
            return False

        player_coords = self.state[STATE.PLAYER_KEY]
        key_coords = self.state[STATE.KEY_DICT_KEY]

        if key_coords is None:
            return False

        return self._coords_are_next_to_each_other(player_coords, key_coords)

    @staticmethod
    def _coords_are_next_to_each_other(point1: (int, int), point2: (int, int)) -> bool:

        return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1]) == 1

    def _pick_up_key(self) -> GridWorldState:

        new_state = self.state.copy()
        new_state[STATE.KEY_DICT_KEY] = None
        new_state[STATE.HAS_KEY_DICT_KEY] = 1
        return GridWorldState(new_state)



