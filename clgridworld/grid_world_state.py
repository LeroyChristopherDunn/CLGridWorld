

class GridWorldState:

    SHAPE_KEY = "shape"
    PLAYER_COORDS_KEY = "player_coords"
    KEY_COORDS_KEY = "key_coords"
    LOCK_COORDS_KEY = "lock_coords"
    PIT_COORDS_KEY = "pit_coords"
    HAS_KEY_KEY = "has_key"

    @staticmethod
    def create(shape: tuple, player_coords: tuple, key_coords: tuple, lock_coords: tuple, pit_coords: tuple) -> dict:

        GridWorldState._validate_coords_are_in_bounds(key_coords, lock_coords, pit_coords, player_coords, shape)
        GridWorldState._validate_coords_dont_overlap(key_coords, lock_coords, pit_coords, player_coords)

        return {
            GridWorldState.SHAPE_KEY: shape,
            GridWorldState.PLAYER_COORDS_KEY: player_coords,
            GridWorldState.KEY_COORDS_KEY: key_coords,
            GridWorldState.LOCK_COORDS_KEY: lock_coords,
            GridWorldState.PIT_COORDS_KEY: pit_coords,
            GridWorldState.HAS_KEY_KEY: 0,
        }

    @staticmethod
    def _validate_coords_are_in_bounds(key_coords, lock_coords, pit_coords, player_coords, shape):

        if not GridWorldState._is_in_bounds(player_coords, shape):
            raise ValueError("Player coords %s not in shape bounds %s" % (player_coords, shape))

        if not GridWorldState._is_in_bounds(key_coords, shape):
            raise ValueError("Key coords %s not in shape bounds %s" % (key_coords, shape))

        if not GridWorldState._is_in_bounds(lock_coords, shape):
            raise ValueError("lock coords %s not in shape bounds %s" % (lock_coords, shape))

        for pit_coord in pit_coords:
            if not GridWorldState._is_in_bounds(pit_coord, shape):
                raise ValueError("lock coords %s not in shape bounds %s" % (pit_coord, shape))

    @staticmethod
    def _validate_coords_dont_overlap(key_coords, lock_coords, pit_coords, player_coords):

        if player_coords == key_coords:
            raise ValueError("player coords %s equal to key coords %s" % (player_coords, key_coords))

        if player_coords == lock_coords:
            raise ValueError("player coords %s equal to lock coords %s" % (player_coords, key_coords))

        if key_coords == lock_coords:
            raise ValueError("key coords %s equal to lock coords %s" % (player_coords, key_coords))

        if pit_coords[0][0] <= player_coords[0] <= pit_coords[1][0] \
                and pit_coords[0][1] <= player_coords[1] < pit_coords[1][1]:
            raise ValueError("player coords %s within pit coords %s" % (player_coords, pit_coords))

        if pit_coords[0][0] <= lock_coords[0] <= pit_coords[1][0] \
                and pit_coords[0][1] <= lock_coords[1] < pit_coords[1][1]:
            raise ValueError("lock coords %s within pit coords %s" % (lock_coords, pit_coords))

        if pit_coords[0][0] <= key_coords[0] <= pit_coords[1][0] \
                and pit_coords[0][1] <= key_coords[1] < pit_coords[1][1]:
            raise ValueError("key coords %s within pit coords %s" % (key_coords, pit_coords))

    @staticmethod
    def _is_in_bounds(point: tuple, shape: tuple) -> bool:
        return 0 <= point[0] < shape[0] and 0 <= point[1] < shape[1]