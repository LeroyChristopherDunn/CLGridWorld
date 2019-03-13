

class GridWorldState:

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

    @staticmethod
    def create(shape: tuple, player_coords: tuple, key_coords: tuple, lock_coords: tuple, pit_start_coords: tuple, pit_end_coords: tuple) -> dict:

        GridWorldState._validate_coords_are_in_bounds(shape, player_coords, key_coords, lock_coords, pit_start_coords, pit_end_coords)
        GridWorldState._validate_coords_dont_overlap(player_coords, key_coords, lock_coords, pit_start_coords, pit_end_coords)

        ne_beacon_coords, nw_beacon_coords, se_beacon_coords, sw_beacon_coords = \
            GridWorldState._get_pit_beacon_coords(pit_start_coords, pit_end_coords)

        return {
            GridWorldState.GRID_SHAPE_KEY:      shape,
            GridWorldState.PLAYER_KEY:          player_coords,
            GridWorldState.KEY_DICT_KEY:        key_coords,
            GridWorldState.LOCK_KEY:            lock_coords,
            GridWorldState.PIT_START_KEY:       pit_start_coords,
            GridWorldState.PIT_END_KEY:         pit_end_coords,
            GridWorldState.NW_BEACON_KEY:       nw_beacon_coords,
            GridWorldState.NE_BEACON_KEY:       ne_beacon_coords,
            GridWorldState.SW_BEACON_KEY:       sw_beacon_coords,
            GridWorldState.SE_BEACON_KEY:       se_beacon_coords,
            GridWorldState.HAS_KEY_DICT_KEY:    0,
        }

    @staticmethod
    def _validate_coords_are_in_bounds(shape, player_coords, key_coords, lock_coords, pit_start_coords, pit_end_coords):

        if not GridWorldState._is_in_shape_bounds(player_coords, shape):
            raise ValueError("Player coords %s not in shape bounds %s" % (player_coords, shape))

        if not GridWorldState._is_in_shape_bounds(key_coords, shape):
            raise ValueError("Key coords %s not in shape bounds %s" % (key_coords, shape))

        if not GridWorldState._is_in_shape_bounds(lock_coords, shape):
            raise ValueError("lock coords %s not in shape bounds %s" % (lock_coords, shape))

        if not GridWorldState._is_in_shape_bounds(pit_start_coords, shape):
            raise ValueError("lock coords %s not in shape bounds %s" % (pit_start_coords, shape))

        if not GridWorldState._is_in_shape_bounds(pit_end_coords, shape):
            raise ValueError("lock coords %s not in shape bounds %s" % (pit_end_coords, shape))

    @staticmethod
    def _validate_coords_dont_overlap(player_coords, key_coords, lock_coords, pit_start_coords, pit_end_coords):

        if player_coords == key_coords:
            raise ValueError("player coords %s equal to key coords %s" % (player_coords, key_coords))

        if player_coords == lock_coords:
            raise ValueError("player coords %s equal to lock coords %s" % (player_coords, key_coords))

        if key_coords == lock_coords:
            raise ValueError("key coords %s equal to lock coords %s" % (player_coords, key_coords))

        pit_row_start = pit_start_coords[0]
        pit_col_start = pit_start_coords[1]
        pit_row_end = pit_end_coords[0]
        pit_col_end = pit_end_coords[1]

        if pit_row_start <= player_coords[0] <= pit_row_end and pit_col_start <= player_coords[1] <= pit_col_end:
            raise ValueError("player coords %s within pit start coords %s and pit end coords %s" % (player_coords, pit_start_coords, pit_end_coords))

        if pit_row_start <= lock_coords[0] <= pit_row_end and pit_col_start <= lock_coords[1] <= pit_col_end:
            raise ValueError("lock coords %s within pit start coords %s and pit end coords %s" % (lock_coords, pit_start_coords, pit_end_coords))

        if pit_row_start <= key_coords[0] <= pit_row_end and pit_col_start <= key_coords[1] <= pit_col_end:
            raise ValueError("key coords %s within pit start coords %s and pit end coords %s" % (key_coords, pit_start_coords, pit_end_coords))

    @staticmethod
    def _is_in_shape_bounds(point: tuple, shape: tuple) -> bool:
        return 0 <= point[0] < shape[0] and 0 <= point[1] < shape[1]

    @staticmethod
    def _get_pit_beacon_coords(pit_start_coords, pit_end_coords):

        pit_row_start = pit_start_coords[0]
        pit_col_start = pit_start_coords[1]
        pit_row_end = pit_end_coords[0]
        pit_col_end = pit_end_coords[1]

        nw_beacon_coords = (pit_row_start - 1, pit_col_start - 1)
        ne_beacon_coords = (pit_row_start - 1, pit_col_end + 1)
        sw_beacon_coords = (pit_row_end + 1, pit_col_start - 1)
        se_beacon_coords = (pit_row_end + 1, pit_col_end + 1)

        return ne_beacon_coords, nw_beacon_coords, se_beacon_coords, sw_beacon_coords
