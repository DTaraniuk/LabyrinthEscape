import pygame
from constants import*
from typing import Tuple
from direction import *
from coordpair import CoordPair


class Cell:
    def __init__(self, row: int, col: int, width: int, total_rows: int):
        self.index_in_row = row
        self.index_in_col = col
        self.width = width
        self._neighbors: dict[Direction, 'Cell'] = {}
        self.total_rows = total_rows
        self.color: Tuple[int, int, int] = WHITE
        self.is_up_to_date = False

    def __lt__(self, other):
        return self.index_in_row + self.index_in_col < other.index_in_row + other.index_in_col

    def is_neighbor(self, other) -> bool:
        return other in self._neighbors.values()

    def get_neighbors(self) -> dict[Direction, 'Cell']:
        return self._neighbors.copy()

    def add_neighbor(self, other: 'Cell', dir_: Direction = None):
        if dir_ is None:
            dir_ = get_direction(self.get_distance(other))
        if dir_ is not None:
            self._neighbors[dir_] = other
            other._neighbors[dir_.opposite()] = self

    def request_update(self):
        self.is_up_to_date = False

    def mark_updated(self):
        self.is_up_to_date = True

    def get_index(self) -> Tuple[int, int]:
        return self.index_in_row, self.index_in_col

    def get_pos(self) -> CoordPair:
        return CoordPair(self.index_in_row * self.width, self.index_in_col * self.width)

    def get_distance(self, other: 'Cell') -> CoordPair:
        return CoordPair(other.index_in_row-self.index_in_row, other.index_in_col-self.index_in_col)

    def draw(self, win: pygame.Surface) -> None:
        if self.is_up_to_date:
            return
        width: int = self.width
        x, y = self.index_in_row * width, self.index_in_col * width
        pygame.draw.rect(win, self.color, (x, y, width, width))

        sides = {Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST}
        for direction in self._neighbors.keys():
            if direction in sides:
                sides.remove(direction)

        for direction in sides:
            wx1: int = x
            wx2: int = x
            wy1: int = y
            wy2: int = y
            if direction == Direction.SOUTH:  # DOWN
                wx2 += width - WALL_WIDTH
                wy1 += width - WALL_WIDTH
                wy2 += width - WALL_WIDTH
            if direction == Direction.NORTH:  # UP
                wx2 += width
            if direction == Direction.EAST:  # RIGHT
                wx1 += width - WALL_WIDTH
                wx2 += width - WALL_WIDTH
                wy2 += width - WALL_WIDTH
            if direction == Direction.WEST:  # LEFT
                wy2 += width
            pygame.draw.line(win, RED, (wx1, wy1), (wx2, wy2), WALL_WIDTH)

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

    def change_color(self, new_color):
        if new_color != self.color:
            self.color = new_color
            self.request_update()
