from enum import Enum
from .coordpair import CoordPair
from typing import Optional
from common.constants import EPS


class Direction(Enum):
    NORTH = CoordPair(0, -1)
    SOUTH = CoordPair(0, 1)
    EAST = CoordPair(1, 0)
    WEST = CoordPair(-1, 0)

    def opposite(self) -> 'Direction':
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.NORTH
        elif self == Direction.EAST:
            return Direction.WEST
        elif self == Direction.WEST:
            return Direction.EAST
        else:
            raise ValueError("Invalid direction")


def get_direction(coord_pair: CoordPair) -> Optional[Direction]:
    for direction in Direction:
        if coord_pair.equals(direction.value):
            return direction
    return None


def get_move_direction(p1: CoordPair, p2: CoordPair) -> CoordPair:
    return CoordPair(x, y)
