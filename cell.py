import pygame
from constants import*
from typing import List, Tuple


class Cell:
    def __init__(self, row: int, col: int, width: int, total_rows: int):
        self.row = row
        self.col = col
        self.width = width
        self.neighbors: List['Cell'] = []
        self.total_rows = total_rows
        self.color: Tuple[int, int, int] = WHITE
        self.is_up_to_date = False

    def __lt__(self, other):
        return self.row+self.col < other.row + other.col

    def request_update(self):
        self.is_up_to_date = False

    def mark_updated(self):
        self.is_up_to_date = True

    def get_pos(self) -> Tuple[int, int]:
        return self.row, self.col

    def draw(self, win: pygame.Surface) -> None:
        if self.is_up_to_date:
            return
        width: int = self.width
        x, y = self.col * width, self.row * width
        pygame.draw.rect(win, self.color, (x, y, width, width))

        sides = {'U', 'D', 'L', 'R'}
        for neighbor in self.neighbors:
            if neighbor.col == self.col and neighbor.row == self.row + 1:  # DOWN
                sides.remove('D')
            if neighbor.col == self.col and neighbor.row == self.row - 1:  # UP
                sides.remove('U')
            if neighbor.col == self.col + 1 and neighbor.row == self.row:  # RIGHT
                sides.remove('R')
            if neighbor.col == self.col - 1 and neighbor.row == self.row:  # LEFT
                sides.remove('L')
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

    def get_center(self) -> tuple[int, int]:
        x = self.col+self.width/2
        y = self.row+self.width/2
        return (x, y)
