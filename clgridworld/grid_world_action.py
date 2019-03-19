from gym import spaces


class GridWorldAction:

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    PICK_UP_KEY = 4
    UNLOCK_LOCK = 5

    NAMES = {
        0: "NORTH",
        1: "EAST",
        2: "SOUTH",
        3: "WEST",
        4: "PICK_UP_KEY",
        5: "UNLOCK_LOCK"
    }


class GridWorldActionSpace(spaces.Discrete):

    def __init__(self):
        super(GridWorldActionSpace, self).__init__(len(GridWorldAction.NAMES))


