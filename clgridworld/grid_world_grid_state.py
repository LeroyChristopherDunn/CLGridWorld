import numpy as np

from clgridworld.grid_world_state import GridWorldState


class GridWorldGridState:

    EMPTY = 0
    PLAYER = 1
    KEY = 2
    LOCK = 3
    PIT = 4
    BEACON = 5

    def __init__(self, state: dict):

        self.state = state

        self.grid_shape = state[GridWorldState.GRID_SHAPE_KEY]
        self.player_coords = state[GridWorldState.PLAYER_KEY]
        self.lock_coords = state[GridWorldState.LOCK_KEY]
        self.key_coords = state[GridWorldState.KEY_DICT_KEY]
        self.pit_start_coords = state[GridWorldState.PIT_START_KEY]
        self.pit_end_coords = state[GridWorldState.PIT_END_KEY]
        self.nw_beacon_coords = state[GridWorldState.NW_BEACON_KEY]
        self.ne_beacon_coords = state[GridWorldState.NE_BEACON_KEY]
        self.sw_beacon_coords = state[GridWorldState.SW_BEACON_KEY]
        self.se_beacon_coords = state[GridWorldState.SE_BEACON_KEY]
        self.has_key = state[GridWorldState.GRID_SHAPE_KEY]

        self.grid = self.create_grid()

    def create_grid(self) -> np.ndarray:

        grid = np.zeros(self.grid_shape, dtype=np.uint16)

        GridWorldGridState._plot_if_not_null(grid, self.player_coords, GridWorldGridState.PLAYER)
        GridWorldGridState._plot_if_not_null(grid, self.key_coords, GridWorldGridState.KEY)
        GridWorldGridState._plot_if_not_null(grid, self.lock_coords, GridWorldGridState.LOCK)

        if self.pit_start_coords is not None and self.pit_end_coords is not None:
            grid[self.pit_start_coords[0]:self.pit_end_coords[0] + 1, self.pit_start_coords[1]:self.pit_end_coords[1] + 1] = GridWorldGridState.PIT

        GridWorldGridState._plot_if_not_null(grid, self.nw_beacon_coords, GridWorldGridState.BEACON)
        GridWorldGridState._plot_if_not_null(grid, self.ne_beacon_coords, GridWorldGridState.BEACON)
        GridWorldGridState._plot_if_not_null(grid, self.sw_beacon_coords, GridWorldGridState.BEACON)
        GridWorldGridState._plot_if_not_null(grid, self.se_beacon_coords, GridWorldGridState.BEACON)

        return grid

    @staticmethod
    def _plot_if_not_null(_grid: np.ndarray, point, char: int):
        if point is not None:
            _grid[point] = char
