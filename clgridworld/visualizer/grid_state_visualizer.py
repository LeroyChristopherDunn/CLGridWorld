import numpy as np

from clgridworld.state.state import GridWorldState


class GridStateVisualizer:

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
        grid[:] = GridStateVisualizer.EMPTY

        GridStateVisualizer._plot_if_not_null(grid, self.state.player, GridStateVisualizer.PLAYER)
        GridStateVisualizer._plot_if_not_null(grid, self.state.key, GridStateVisualizer.KEY)
        GridStateVisualizer._plot_if_not_null(grid, self.state.lock, GridStateVisualizer.LOCK)

        if self.state.pit_start is not None and self.state.pit_end is not None:
            grid[self.state.pit_start[0]:self.state.pit_end[0] + 1, self.state.pit_start[1]:self.state.pit_end[1] + 1] = GridStateVisualizer.PIT

        GridStateVisualizer._plot_if_not_null(grid, self.state.nw_beacon, GridStateVisualizer.BEACON)
        GridStateVisualizer._plot_if_not_null(grid, self.state.ne_beacon, GridStateVisualizer.BEACON)
        GridStateVisualizer._plot_if_not_null(grid, self.state.sw_beacon, GridStateVisualizer.BEACON)
        GridStateVisualizer._plot_if_not_null(grid, self.state.se_beacon, GridStateVisualizer.BEACON)

        return grid

    @staticmethod
    def _plot_if_not_null(_grid: np.ndarray, point, char):
        if point is not None:
            _grid[point] = char
