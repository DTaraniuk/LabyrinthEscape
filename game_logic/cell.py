from common.constants import *
from typing import Tuple
from .direction import *
from .coordpair import CoordPair


class Cell:
    def __init__(self, row: int, col: int, width: int, total_rows: int):
        self.index_in_row = row
        self.index_in_col = col
        self.width = width
        self._neighbors: dict[str, 'Cell'] = {}
        self.total_rows = total_rows
        self._color: Tuple[int, int, int] = WHITE
        self._is_updated = False

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

    def get_neighbors(self) -> dict[str, 'Cell']:
        return self._neighbors.copy()

    def add_neighbor(self, other: 'Cell', dir_: str = None):
        if dir_ is None:
            dir_ = get_direction(self.get_distance(other))
        if dir_ is not None:
            self._neighbors[dir_.name] = other
            other._neighbors[dir_.opposite().name] = self

    @property
    def is_updated(self):
        return self._is_updated

    @is_updated.setter
    def is_updated(self, value):
        self._is_updated = value

    def get_index(self) -> Tuple[int, int]:
        return self.index_in_row, self.index_in_col

    def get_pos(self) -> CoordPair:
        return CoordPair(self.index_in_row * self.width, self.index_in_col * self.width)

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

