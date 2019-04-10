import numpy as np

from clgridworld.grid_world_state import GridWorldState


class GridWorldGridState:

    EMPTY = '-'
    PLAYER = 'P'
    KEY = 'K'
    LOCK = 'L'
    PIT = 'X'
    BEACON = 'B'

    def __init__(self, state: GridWorldState):

        self.state = state

        self.grid = self._create_grid()

    def _create_grid(self) -> np.ndarray:

        grid = np.chararray(self.state.grid_shape, unicode=True)
        grid[:] = GridWorldGridState.EMPTY

        GridWorldGridState._plot_if_not_null(grid, self.state.player, GridWorldGridState.PLAYER)
        GridWorldGridState._plot_if_not_null(grid, self.state.key, GridWorldGridState.KEY)
        GridWorldGridState._plot_if_not_null(grid, self.state.lock, GridWorldGridState.LOCK)

        if self.state.pit_start is not None and self.state.pit_end is not None:
            grid[self.state.pit_start[0]:self.state.pit_end[0] + 1, self.state.pit_start[1]:self.state.pit_end[1] + 1] = GridWorldGridState.PIT

        GridWorldGridState._plot_if_not_null(grid, self.state.nw_beacon, GridWorldGridState.BEACON)
        GridWorldGridState._plot_if_not_null(grid, self.state.ne_beacon, GridWorldGridState.BEACON)
        GridWorldGridState._plot_if_not_null(grid, self.state.sw_beacon, GridWorldGridState.BEACON)
        GridWorldGridState._plot_if_not_null(grid, self.state.se_beacon, GridWorldGridState.BEACON)

        return grid

    @staticmethod
    def _plot_if_not_null(_grid: np.ndarray, point, char):
        if point is not None:
            _grid[point] = char
