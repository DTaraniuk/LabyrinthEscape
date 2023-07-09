from common.constants import *
from typing import Tuple
from game_logic.direction import *
from game_logic.coordpair import CoordPair
from .wall import Wall


class Cell:
    def __init__(self, row: int, col: int, width: int):
        self.index_in_row = row
        self.index_in_col = col
        self.width = width
        self._neighbors: dict[Direction, 'Cell'] = {}
        self._walls: dict[Direction, Wall] = {}
        self._color: Tuple[int, int, int] = WHITE
        self.is_updated = False  # if the cell needs to be redrawn

    def __lt__(self, other):
        return self.index_in_row + self.index_in_col < other.index_in_row + other.index_in_col

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value != self._color:
            self._color = value
            self.is_updated = False

    def is_neighbor(self, other) -> bool:
        return other in self._neighbors.values()

    def get_neighbors(self) -> dict[Direction, 'Cell']:
        return self._neighbors.copy()

    # also removes wall
    def add_neighbor(self, other: 'Cell', direction: Direction = None):
        if direction is None:
            direction = get_direction(self.get_distance(other))

        if self._neighbors.get(direction):
            return

        opp_direction = direction.opposite()

        self._neighbors[direction] = other
        other._neighbors[opp_direction] = self

        wall = self._walls.get(direction)
        if wall:
            self._walls.pop(direction)
            other._walls.pop(opp_direction)

    def get_walls(self) -> dict[Direction, Wall]:
        return self._walls.copy()

    # also removes neighbor
    def add_wall(self, wall: Wall, direction: Direction):
        if self._walls.get(direction):
            return

        opp_direction = direction.opposite()

        self._walls[direction] = wall
        neighbor = self._neighbors.get(direction)
        if neighbor:
            neighbor._walls[opp_direction] = wall
            self._neighbors.pop(direction)
            neighbor._neighbors.pop(opp_direction)

    def get_index(self) -> Tuple[int, int]:
        return self.index_in_row, self.index_in_col

    def get_pos(self) -> CoordPair:
        return CoordPair(self.index_in_row * self.width, self.index_in_col * self.width)

    def get_x(self):
        return self.index_in_row * self.width

    def get_y(self):
        return self.index_in_col * self.width

    def get_distance(self, other: 'Cell') -> CoordPair:
        return CoordPair(other.index_in_row-self.index_in_row, other.index_in_col-self.index_in_col)

    def get_center(self) -> CoordPair:
        x = (self.index_in_row + 0.5)*self.width
        y = (self.index_in_col + 0.5)*self.width
        return CoordPair(x, y)

    def get_visible_cells(self) -> list['Cell']:
        res = [self]
        for dir_, neighbor in self.get_neighbors().items():
            res.append(neighbor)
            while dir_ in neighbor.get_neighbors().keys():
                neighbor = neighbor.get_neighbors()[dir_]
                res.append(neighbor)
        return res

