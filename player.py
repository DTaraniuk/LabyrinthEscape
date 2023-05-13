import math
from typing import Tuple
import pygame
from constants import*
from maze import Maze
from coordpair import CoordPair
from direction import Direction


class Player:
    def __init__(self, pos: CoordPair, size: Tuple[int, int], img: pygame.Surface = None):
        self._x: float = pos.x
        self._y: float = pos.y
        self.size = size
        self.speed = PLAYER_SPEED
        if img is not None:
            player_surface = img.convert_alpha()
            resized_player_surface = pygame.transform.scale(player_surface, self.size)
            self.image = resized_player_surface
        else:
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            self.image.fill(PINK)

    def set_pos(self, coords: CoordPair):
        self._x, self._y = coords

    def get_pos(self) -> CoordPair:
        return CoordPair(self._x, self._y)

    def center(self, x, y):
        size_x, size_y = self.size
        self._x = x - size_x / 2
        self._y = y - size_y / 2

    def get_center(self) -> CoordPair:
        size_x, size_y = self.size
        return CoordPair(self._x + size_x / 2, self._y + size_y / 2)

    def player_move(self, vector: CoordPair, maze: Maze) -> bool:
        self.move(vector, maze)
        current_cell = maze.get_cell(self.get_center())
        if current_cell == maze.victory_cell:
            return True
        return False

    def move(self, vector: CoordPair, maze: Maze):
        x, y = self.get_center()
        current_cell = maze.get_cell(CoordPair(x, y))
        current_cell.request_update()
        dx, dy = vector

        target_x = min(maze.width - 1, x + dx * self.speed)
        target_y = min(maze.width - 1, y + dy * self.speed)

        target_x_cell = maze.get_cell(CoordPair(target_x, y))
        target_y_cell = maze.get_cell(CoordPair(x, target_y))

        curr_x, curr_y = current_cell.get_pos()
        if current_cell != target_x_cell:
            if not current_cell.is_neighbor(target_x_cell):
                if dx > 0:  # moving right
                    target_x = curr_x + current_cell.width - 1
                else:  # moving left
                    target_x = curr_x
            else:
                target_x_cell.request_update()

        if current_cell != target_y_cell:
            if not current_cell.is_neighbor(target_y_cell):
                if dy > 0:  # moving down
                    target_y = curr_y + current_cell.width - 1
                else:  # moving up
                    target_y = curr_y
            else:
                target_y_cell.request_update()

        self.center(target_x, target_y)


