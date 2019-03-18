from clgridworld.grid_world_actions import GridWorldActions
from clgridworld.grid_world_state import GridWorldState


class GridWorldDynamics:

    def __init__(self, state):
        self.state = state

    def step(self, action) -> dict:  # this should return a state

        if self._player_moves_into_boundary(action):
            return self.state.copy()

        return self._move_player(action)

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

    def _move_player(self, action):

        new_state = self.state.copy()
        player_coords = self.state[GridWorldState.PLAYER_KEY]

        if action == GridWorldActions.NORTH:
            new_state[GridWorldState.PLAYER_KEY] = (player_coords[0] - 1, player_coords[1])

        elif action == GridWorldActions.EAST:
            new_state[GridWorldState.PLAYER_KEY] = (player_coords[0], player_coords[1] + 1)

        elif action == GridWorldActions.SOUTH:
            new_state[GridWorldState.PLAYER_KEY] = (player_coords[0] + 1, player_coords[1])

        elif action == GridWorldActions.WEST:
            new_state[GridWorldState.PLAYER_KEY] = (player_coords[0], player_coords[1] - 1)

        return new_state


