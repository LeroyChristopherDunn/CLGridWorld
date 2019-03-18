from clgridworld.grid_world_state import GridWorldState


class GridWorldReward:
    NO_MOVEMENT = -10
    PLAYER_MOVED_INTO_EMPTY_SPACE = -10
    PLAYER_PICKED_UP_KEY = 500
    PLAYER_UNLOCKED_LOCK = 1000
    PLAYER_MOVED_INTO_PIT = -200


class GridWorldRewardCalculator:

    def calculate(self, curr_state: GridWorldState, next_state: GridWorldState) -> int:

        if curr_state.is_in_pit() != next_state.is_in_pit():
            return GridWorldReward.PLAYER_MOVED_INTO_PIT

        if curr_state.player != next_state.player:
            return GridWorldReward.PLAYER_MOVED_INTO_EMPTY_SPACE

        if curr_state.has_key != next_state.has_key:
            return GridWorldReward.PLAYER_PICKED_UP_KEY

        if curr_state.lock != next_state.lock:
            return GridWorldReward.PLAYER_UNLOCKED_LOCK

        return GridWorldReward.NO_MOVEMENT
