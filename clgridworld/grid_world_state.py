
class GridWorldStateKey:

    GRID_SHAPE_KEY = "grid_shape"
    PLAYER_KEY = "player"
    KEY_DICT_KEY = "key"
    LOCK_KEY = "lock"
    PIT_START_KEY = "pit_start"
    PIT_END_KEY = "pit_end"
    NW_BEACON_KEY = "nw_beacon"
    NE_BEACON_KEY = "ne_beacon"
    SW_BEACON_KEY = "sw_beacon"
    SE_BEACON_KEY = "se_beacon"
    HAS_KEY_DICT_KEY = "has_key"


class GridWorldState:

    @staticmethod
    def create(shape: (int, int), player_coords: (int, int), key_coords: (int, int)=None, lock_coords: (int, int)=None,
               pit_start_coords: (int, int)=None, pit_end_coords: (int, int)=None) -> dict:

        ne_beacon_coords, nw_beacon_coords, se_beacon_coords, sw_beacon_coords = \
            GridWorldState._get_pit_beacon_coords(shape, pit_start_coords, pit_end_coords)

        _GridWorldStateValidator(shape, player_coords, key_coords, lock_coords, pit_start_coords, pit_end_coords,
                                 ne_beacon_coords, nw_beacon_coords, se_beacon_coords, sw_beacon_coords).validate()

        has_key = 1 if key_coords is None else 0

        return {
            GridWorldStateKey.GRID_SHAPE_KEY:      shape,
            GridWorldStateKey.PLAYER_KEY:          player_coords,
            GridWorldStateKey.KEY_DICT_KEY:        key_coords,
            GridWorldStateKey.LOCK_KEY:            lock_coords,
            GridWorldStateKey.PIT_START_KEY:       pit_start_coords,
            GridWorldStateKey.PIT_END_KEY:         pit_end_coords,
            GridWorldStateKey.NW_BEACON_KEY:       nw_beacon_coords,
            GridWorldStateKey.NE_BEACON_KEY:       ne_beacon_coords,
            GridWorldStateKey.SW_BEACON_KEY:       sw_beacon_coords,
            GridWorldStateKey.SE_BEACON_KEY:       se_beacon_coords,
            GridWorldStateKey.HAS_KEY_DICT_KEY:    has_key,
        }

    @staticmethod
    def _get_pit_beacon_coords(shape, pit_start_coords, pit_end_coords):

        if pit_start_coords is None or pit_end_coords is None:
            return None, None, None, None

        pit_row_start = pit_start_coords[0]
        pit_col_start = pit_start_coords[1]
        pit_row_end = pit_end_coords[0]
        pit_col_end = pit_end_coords[1]

        nw_beacon_coords = (pit_row_start - 1, pit_col_start - 1)
        ne_beacon_coords = (pit_row_start - 1, pit_col_end + 1)
        sw_beacon_coords = (pit_row_end + 1, pit_col_start - 1)
        se_beacon_coords = (pit_row_end + 1, pit_col_end + 1)

        if not _GridWorldStateValidator.is_in_shape_bounds(nw_beacon_coords, shape):
            nw_beacon_coords = None

        if not _GridWorldStateValidator.is_in_shape_bounds(ne_beacon_coords, shape):
            ne_beacon_coords = None

        if not _GridWorldStateValidator.is_in_shape_bounds(sw_beacon_coords, shape):
            sw_beacon_coords = None

        if not _GridWorldStateValidator.is_in_shape_bounds(se_beacon_coords, shape):
            se_beacon_coords = None

        return ne_beacon_coords, nw_beacon_coords, se_beacon_coords, sw_beacon_coords


class _GridWorldStateValidator:

    def __init__(self, grid_shape: (int, int), player: (int, int), key: (int, int), lock: (int, int),
                 pit_start: (int, int), pit_end: (int, int), ne_beacon: (int, int), nw_beacon: (int, int),
                 se_beacon: (int, int), sw_beacon: (int, int)):

        self.grid_shape = grid_shape
        self.player = player
        self.pit_end = pit_end
        self.pit_start = pit_start
        self.lock = lock
        self.key = key
        self.ne_beacon = ne_beacon
        self.nw_beacon = nw_beacon
        self.se_beacon = se_beacon
        self.sw_beacon = sw_beacon

    def validate(self):
        self._validate_key_lock_pairing()
        self._validate_pit_coords_pairing()
        self._validate_coords_are_in_bounds()
        self._validate_basic_coords_dont_overlap()
        self._validate_coords_dont_overlap_with_pit()
        self._validate_coords_dont_overlap_with_beacons()

    def _validate_key_lock_pairing(self):

        if self.key is None and self.lock is None:
            raise ValueError("key or lock coords required")

    def _validate_pit_coords_pairing(self):

        if type(self.pit_start) != type(self.pit_end):
            raise ValueError("invalid pit coords, start %s end %s" % (self.pit_start, self.pit_end))

    def _validate_coords_are_in_bounds(self):

        if not self.is_in_shape_bounds(self.player, self.grid_shape):
            raise ValueError("player coords %s not in grid_shape bounds %s" % (self.player, self.grid_shape))

        if self.key is not None and not self.is_in_shape_bounds(self.key, self.grid_shape):
            raise ValueError("key coords %s not in grid_shape bounds %s" % (self.key, self.grid_shape))

        if self.lock is not None and not self.is_in_shape_bounds(self.lock, self.grid_shape):
            raise ValueError("lock coords %s not in grid_shape bounds %s" % (self.lock, self.grid_shape))

        if self.pit_start is not None and not self.is_in_shape_bounds(self.pit_start, self.grid_shape):
            raise ValueError("lock coords %s not in grid_shape bounds %s" % (self.pit_start, self.grid_shape))

        if self.pit_end is not None and not self.is_in_shape_bounds(self.pit_end, self.grid_shape):
            raise ValueError("lock coords %s not in grid_shape bounds %s" % (self.pit_end, self.grid_shape))

    @staticmethod
    def is_in_shape_bounds(point: (int, int), shape: (int, int)) -> bool:
        return 0 <= point[0] < shape[0] and 0 <= point[1] < shape[1]

    def _validate_basic_coords_dont_overlap(self):

        if self.player == self.key:
            raise ValueError("player coords %s equal to key coords %s" % (self.player, self.key))

        if self.player == self.lock:
            raise ValueError("player coords %s equal to lock coords %s" % (self.player, self.lock))

        if self.key == self.lock:
            raise ValueError("key coords %s equal to lock coords %s" % (self.key, self.lock))

    def _validate_coords_dont_overlap_with_pit(self):

        if self.pit_start is None and self.pit_end is None:
            return

        pit_row_start = self.pit_start[0]
        pit_col_start = self.pit_start[1]
        pit_row_end = self.pit_end[0]
        pit_col_end = self.pit_end[1]

        if pit_row_start <= self.player[0] <= pit_row_end and pit_col_start <= self.player[1] <= pit_col_end:
            raise ValueError("player coords %s within pit start coords %s and pit end coords %s" %
                             (self.player, self.pit_start, self.pit_end))

        if self.lock is not None and pit_row_start <= self.lock[0] <= pit_row_end and pit_col_start <= self.lock[1] <= pit_col_end:
            raise ValueError("lock coords %s within pit start coords %s and pit end coords %s" %
                             (self.lock, self.pit_start, self.pit_end))

        if self.key is not None and pit_row_start <= self.key[0] <= pit_row_end and pit_col_start <= self.key[1] <= pit_col_end:
            raise ValueError("key coords %s within pit start coords %s and pit end coords %s" %
                             (self.key, self.pit_start, self.pit_end))

    def _validate_coords_dont_overlap_with_beacons(self):

        beacons = [self.ne_beacon, self.nw_beacon, self.se_beacon, self.sw_beacon]

        for beacon in beacons:

            if self.player == beacon:
                raise ValueError("player coords %s overlap with pit beacon coords %s" % (self.player, beacon))

            if self.lock == beacon:
                raise ValueError("lock coords %s overlap with pit beacon coords %s" % (self.lock, beacon))

            if self.key == beacon:
                raise ValueError("key coords %s overlap with pit beacon coords %s" % (self.key, beacon))

