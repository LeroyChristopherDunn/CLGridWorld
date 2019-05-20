from typing import NamedTuple

from clgridworld.state.state import GridWorldState


class GridWorldReward(NamedTuple):
    no_movement: int = -10
    player_moved_into_empty_space: int = -10
    player_picked_up_key: int = 500
    player_unlocked_lock: int = 1000
    player_moved_into_pit: int = -200


class GridWorldRewardFunction:

    def __init__(self, reward: GridWorldReward = GridWorldReward()):
        self.reward = reward

    def calculate(self, curr_state: GridWorldState, next_state: GridWorldState) -> int:

        if curr_state.is_in_pit() != next_state.is_in_pit():
            return self.reward.player_moved_into_pit

        if curr_state.player != next_state.player:
            return self.reward.player_moved_into_empty_space

        if curr_state.has_key != next_state.has_key:
            return self.reward.player_picked_up_key

        if curr_state.lock != next_state.lock:
            return self.reward.player_unlocked_lock

        return self.reward.no_movement
