from collections import OrderedDict
from typing import Tuple

import numpy as np
from clgridworld.state.state import GridWorldState

_cache = OrderedDict()

class EuclideanDistanceCalculator:

    def __init__(self, state: GridWorldState):
        self.state = state

    def distance_to_key(self)->float:
        return self._player_distance_to_item(self.state.key)

    def distance_to_lock(self)->float:
        return self._player_distance_to_item(self.state.lock)

    def distance_to_closest_beacon(self)->float:

        beacons = [self.state.nw_beacon, self.state.ne_beacon, self.state.sw_beacon, self.state.se_beacon]
        beacons = list(filter(lambda beacon: beacon is not None, beacons))

        if len(beacons) == 0:
            return 0

        distances = list(map(lambda beacon: self._player_distance_to_item(beacon), beacons))
        return min(distances)

    def _player_distance_to_item(self, item)->float:

        if item is None:
            return 0

        return EuclideanDistanceCalculator.distance(self.state.player, item)

    @staticmethod
    def distance(x: Tuple[int, int], y: Tuple[int, int])->float:

        x, y = EuclideanDistanceCalculator._sort(x, y)

        key = x.__hash__() + y.__hash__()

        if key not in _cache:
            value = np.linalg.norm(np.asarray(x) - np.asarray(y))
            _cache[key] = value

        return _cache[key]

    @staticmethod
    def _sort(x: Tuple[int, int], y: Tuple[int, int]):

        should_swap = False

        if x[0] > y[0]:
            should_swap = True

        if x[0] == y[0] and x[1] > y[1]:
            should_swap = True

        return (y , x) if should_swap else (x , y)

