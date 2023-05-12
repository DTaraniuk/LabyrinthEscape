import pygame
from constants import*
from typing import Tuple


class Cell:
    def __init__(self, row: int, col: int, width: int, total_rows: int):
        self.index_in_row = row
        self.index_in_col = col
        self.width = width
        self._neighbors: set['Cell'] = set()
        self.total_rows = total_rows
        self.color: Tuple[int, int, int] = WHITE
        self.is_up_to_date = False

    def __lt__(self, other):
        return self.index_in_row + self.index_in_col < other.index_in_row + other.index_in_col

    def is_neighbor(self, other) -> bool:
        return other in self._neighbors

    def get_neighbors(self) -> list['Cell']:
        res = []
        res.extend(self._neighbors)
        return res

    def add_neighbor(self, other: 'Cell'):
        self._neighbors.add(other)
        other._neighbors.add(self)

    def request_update(self):
        self.is_up_to_date = False

    def mark_updated(self):
        self.is_up_to_date = True

    def get_index(self) -> Tuple[int, int]:
        return self.index_in_row, self.index_in_col

    def get_pos(self) -> Tuple[float, float]:
        return self.index_in_row * self.width, self.index_in_col * self.width

    def draw(self, win: pygame.Surface) -> None:
        if self.is_up_to_date:
            return
        width: int = self.width
        x, y = self.index_in_row * width, self.index_in_col * width
        pygame.draw.rect(win, self.color, (x, y, width, width))

        sides = {'U', 'D', 'L', 'R'}
        for neighbor in self._neighbors:
            if neighbor.index_in_col == self.index_in_col and neighbor.index_in_row == self.index_in_row + 1:  # RIGHT
                sides.remove('R')
            if neighbor.index_in_col == self.index_in_col and neighbor.index_in_row == self.index_in_row - 1:  # LEFT
                sides.remove('L')
            if neighbor.index_in_col == self.index_in_col + 1 and neighbor.index_in_row == self.index_in_row:  # DOWN
                sides.remove('D')
            if neighbor.index_in_col == self.index_in_col - 1 and neighbor.index_in_row == self.index_in_row:  # UP
                sides.remove('U')
        for i in sides:
            wx1: int = x
            wx2: int = x
            wy1: int = y
            wy2: int = y
            if 'D' == i:  # DOWN
                wx2 += width
                wy1 += width
                wy2 += width
            if 'U' == i:  # UP
                wx2 += width
            if 'R' == i:  # RIGHT
                wx1 += width
                wx2 += width
                wy2 += width
            if 'L' == i:  # LEFT
                wy2 += width
            pygame.draw.line(win, BLACK, (wx1, wy1), (wx2, wy2), WALL_WIDTH*2)

    def get_center(self) -> tuple[float, float]:
        x = self.index_in_col + self.width / 2
        y = self.index_in_row + self.width / 2
        return x, y
