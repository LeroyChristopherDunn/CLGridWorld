from typing import NamedTuple, Tuple, Optional

from gym import spaces

_NONE = (-1. - 1)


class GridWorldState(NamedTuple):
    grid_shape: Tuple[int, int]
    player: Tuple[int, int]
    key: Optional[Tuple[int, int]]
    lock: Optional[Tuple[int, int]]
    pit_start: Optional[Tuple[int, int]]
    pit_end: Optional[Tuple[int, int]]
    nw_beacon: Optional[Tuple[int, int]]
    ne_beacon: Optional[Tuple[int, int]]
    sw_beacon: Optional[Tuple[int, int]]
    se_beacon: Optional[Tuple[int, int]]
    has_key: bool

    def is_in_pit(self) -> bool:
        player = self.player
        pit_start = self.pit_start
        pit_end = self.pit_end

        if pit_start is None and pit_end is None:
            return False

        pit_row_start = pit_start[0]
        pit_col_start = pit_start[1]
        pit_row_end = pit_end[0]
        pit_col_end = pit_end[1]

        return pit_row_start <= player[0] <= pit_row_end and pit_col_start <= player[1] <= pit_col_end

    def player_has_key(self):
        return self.has_key

    def lock_is_unlocked(self):
        return self.lock is None

    def __hash__(self) -> int:
        return self.__str__().__hash__()

    def copy(self,
             grid_shape: Tuple[int, int] = _NONE,
             player: Tuple[int, int] = _NONE,
             key: Tuple[int, int] = _NONE,
             lock: Tuple[int, int] = _NONE,
             pit_start: Tuple[int, int] = _NONE,
             pit_end: Tuple[int, int] = _NONE,
             nw_beacon: Tuple[int, int] = _NONE,
             ne_beacon: Tuple[int, int] = _NONE,
             sw_beacon: Tuple[int, int] = _NONE,
             se_beacon: Tuple[int, int] = _NONE,
             has_key: int = _NONE):
        grid_shape = self.grid_shape if grid_shape == _NONE else grid_shape
        player = self.player if player == _NONE else player
        key = self.key if key == _NONE else key
        lock = self.lock if lock == _NONE else lock
        pit_start = self.pit_start if pit_start == _NONE else pit_start
        pit_end = self.pit_end if pit_end == _NONE else pit_end
        nw_beacon = self.nw_beacon if nw_beacon == _NONE else nw_beacon
        ne_beacon = self.ne_beacon if ne_beacon == _NONE else ne_beacon
        sw_beacon = self.sw_beacon if sw_beacon == _NONE else sw_beacon
        se_beacon = self.se_beacon if se_beacon == _NONE else se_beacon
        has_key = self.has_key if has_key == _NONE else has_key

        return GridWorldState(grid_shape, player, key, lock, pit_start, pit_end,
                              nw_beacon, ne_beacon, sw_beacon, se_beacon, has_key)


class GridWorldObservationSpace(spaces.Tuple):

    def __init__(self, grid_size: (int, int)):
        coords_space = spaces.Tuple((spaces.Discrete(grid_size[0]), spaces.Discrete(grid_size[1])))
        bool_space = spaces.Discrete(2)

        super(GridWorldObservationSpace, self).__init__((
            coords_space,  # grid shape
            coords_space,  # player
            coords_space,  # key
            coords_space,  # lock
            coords_space,  # pit start
            coords_space,  # pit end
            coords_space,  # nw beacon
            coords_space,  # ne beacon
            coords_space,  # sw beacon
            coords_space,  # se beacon
            bool_space  # has key
        ))
