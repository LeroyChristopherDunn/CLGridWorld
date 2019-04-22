from clgridworld.action.action import GridWorldAction as ACTIONS
from clgridworld.state.state import GridWorldState
from clgridworld.state.validator import TerminalStateValidator


class GridWorldDynamics:

    def __init__(self, state: GridWorldState):

        self.state = state
        self._immovable_objects = [state.key, state.lock,
                                   state.nw_beacon, state.ne_beacon,
                                   state.sw_beacon, state.se_beacon].copy()

    def step(self, action) -> GridWorldState:

        if self._is_terminal_state():
            raise Exception("state is terminal state. No further actions allowed")

        if self._player_moves_into_boundary(action):
            return self._clone_state()

        if self._player_moves_into_immovable_object(action):
            return self._clone_state()

        if self._player_picks_up_key_from_eligible_coords(action):
            return self._pick_up_key()

        if self._player_unlocks_lock_from_eligible_state(action):
            return self._unlock_lock()

        return self._translate_player(action)

    def _clone_state(self):
        return self.state.copy()

    def _translate_player(self, action) -> GridWorldState:

        player_coords = self.state.player
        new_player_coords = GridWorldDynamics._translate_coords(player_coords, action)
        return self.state.copy(player=new_player_coords)

    def _player_moves_into_boundary(self, action) -> bool:

        player_coords = self.state.player
        shape = self.state.grid_shape

        if action == ACTIONS.NORTH:
            return player_coords[0] == 0

        elif action == ACTIONS.EAST:
            return player_coords[1] == shape[1] - 1

        elif action == ACTIONS.SOUTH:
            return player_coords[0] == shape[0] - 1

        elif action == ACTIONS.WEST:
            return player_coords[1] == 0

        return False

    def _player_moves_into_immovable_object(self, action) -> bool:

        player_coords = self.state.player
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

    def _player_picks_up_key_from_eligible_coords(self, action) -> bool:

        player_coords = self.state.player
        key_coords = self.state.key

        if action != ACTIONS.PICK_UP_KEY:
            return False

        if key_coords is None:
            return False

        return self._coords_are_next_to_each_other(player_coords, key_coords)

    @staticmethod
    def _coords_are_next_to_each_other(point1: (int, int), point2: (int, int)) -> bool:

        return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1]) == 1

    def _pick_up_key(self) -> GridWorldState:

        return self.state.copy(key=None, has_key=1)

    def _player_unlocks_lock_from_eligible_state(self, action) -> bool:

        player_coords = self.state.player
        key_coords = self.state.key
        lock_coords = self.state.lock

        if action != ACTIONS.UNLOCK_LOCK:
            return False

        if key_coords is not None:
            return False

        return self._coords_are_next_to_each_other(player_coords, lock_coords)

    def _unlock_lock(self) -> GridWorldState:

        return self.state.copy(lock=None)

    def _is_terminal_state(self) -> bool:
        return TerminalStateValidator.is_terminal_state(self.state)


