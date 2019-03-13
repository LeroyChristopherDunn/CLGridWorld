

class GridWorldState:

    SHAPE_KEY = "shape"
    PLAYER_COORDS_KEY = "player_coords"
    KEY_COORDS_KEY = "key_coords"
    LOCK_COORDS_KEY = "lock_coords"
    PIT_COORDS_KEY = "pit_coords"
    HAS_KEY_KEY = "has_key"
    NW_BEACON_COORDS_KEY = "nw_beacon_coords"
    NE_BEACON_COORDS_KEY = "ne_beacon_coords"
    SW_BEACON_COORDS_KEY = "sw_beacon_coords"
    SE_BEACON_COORDS_KEY = "se_beacon_coords"

    @staticmethod
    def create(shape: tuple, player_coords: tuple, key_coords: tuple, lock_coords: tuple, pit_coords: tuple) -> dict:

        GridWorldState._validate_coords_are_in_bounds(key_coords, lock_coords, pit_coords, player_coords, shape)
        GridWorldState._validate_coords_dont_overlap(key_coords, lock_coords, pit_coords, player_coords)

        ne_beacon_coords, nw_beacon_coords, se_beacon_coords, sw_beacon_coords = \
            GridWorldState._get_pit_beacon_coords(pit_coords)

        return {
            GridWorldState.SHAPE_KEY: shape,
            GridWorldState.PLAYER_COORDS_KEY: player_coords,
            GridWorldState.KEY_COORDS_KEY: key_coords,
            GridWorldState.LOCK_COORDS_KEY: lock_coords,
            GridWorldState.PIT_COORDS_KEY: pit_coords,
            GridWorldState.NW_BEACON_COORDS_KEY: nw_beacon_coords,
            GridWorldState.NE_BEACON_COORDS_KEY: ne_beacon_coords,
            GridWorldState.SW_BEACON_COORDS_KEY: sw_beacon_coords,
            GridWorldState.SE_BEACON_COORDS_KEY: se_beacon_coords,
            GridWorldState.HAS_KEY_KEY: 0,
        }

    @staticmethod
    def _validate_coords_are_in_bounds(key_coords, lock_coords, pit_coords, player_coords, shape):

        if not GridWorldState._is_in_shape_bounds(player_coords, shape):
            raise ValueError("Player coords %s not in shape bounds %s" % (player_coords, shape))

        if not GridWorldState._is_in_shape_bounds(key_coords, shape):
            raise ValueError("Key coords %s not in shape bounds %s" % (key_coords, shape))

        if not GridWorldState._is_in_shape_bounds(lock_coords, shape):
            raise ValueError("lock coords %s not in shape bounds %s" % (lock_coords, shape))

        for pit_coord in pit_coords:
            if not GridWorldState._is_in_shape_bounds(pit_coord, shape):
                raise ValueError("lock coords %s not in shape bounds %s" % (pit_coord, shape))

    @staticmethod
    def _validate_coords_dont_overlap(key_coords, lock_coords, pit_coords, player_coords):

        if player_coords == key_coords:
            raise ValueError("player coords %s equal to key coords %s" % (player_coords, key_coords))

        if player_coords == lock_coords:
            raise ValueError("player coords %s equal to lock coords %s" % (player_coords, key_coords))

        if key_coords == lock_coords:
            raise ValueError("key coords %s equal to lock coords %s" % (player_coords, key_coords))

        pit_row_start_incl = pit_coords[0][0]
        pit_col_start_incl = pit_coords[0][1]
        pit_row_end_excl = pit_coords[1][0]
        pit_col_end_excl = pit_coords[1][1]

        if pit_row_start_incl <= player_coords[0] <= pit_row_end_excl \
                and pit_col_start_incl <= player_coords[1] < pit_col_end_excl:
            raise ValueError("player coords %s within pit coords %s" % (player_coords, pit_coords))

        if pit_row_start_incl <= lock_coords[0] <= pit_row_end_excl \
                and pit_col_start_incl <= lock_coords[1] < pit_col_end_excl:
            raise ValueError("lock coords %s within pit coords %s" % (lock_coords, pit_coords))

        if pit_row_start_incl <= key_coords[0] <= pit_row_end_excl \
                and pit_col_start_incl <= key_coords[1] < pit_col_end_excl:
            raise ValueError("key coords %s within pit coords %s" % (key_coords, pit_coords))

    @staticmethod
    def _is_in_shape_bounds(point: tuple, shape: tuple) -> bool:
        return 0 <= point[0] < shape[0] and 0 <= point[1] < shape[1]

    @staticmethod
    def _get_pit_beacon_coords(pit_coords):

        pit_row_start_incl = pit_coords[0][0]
        pit_col_start_incl = pit_coords[0][1]
        pit_row_end_excl = pit_coords[1][0]
        pit_col_end_excl = pit_coords[1][1]

        nw_beacon_coords = (pit_row_start_incl - 1, pit_col_start_incl - 1)
        ne_beacon_coords = (pit_row_start_incl - 1, pit_col_end_excl)
        sw_beacon_coords = (pit_row_end_excl, pit_col_start_incl - 1)
        se_beacon_coords = (pit_row_end_excl, pit_col_end_excl)

        return ne_beacon_coords, nw_beacon_coords, se_beacon_coords, sw_beacon_coords