import math
from typing import Tuple
import pygame
from constants import*
from maze import Maze
from coordpair import CoordPair


class Player:
    def __init__(self, x: int, y: int, size: Tuple[int, int], img: pygame.Surface = None):
        self.x: float = x
        self.y: float = y
        self.size = size
        self.speed = PLAYER_SPEED
        if img is not None:
            player_surface = img.convert_alpha()
            resized_player_surface = pygame.transform.scale(player_surface, self.size)
            self.image = resized_player_surface
        else:
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            self.image.fill(PINK)

    def center(self, x, y):
        size_x, size_y = self.size
        self.x = x - size_x/2
        self.y = y - size_y/2

    def get_center(self):
        size_x, size_y = self.size
        return self.x + size_x/2, self.y + size_y/2

    def move(self, vector: CoordPair, maze: Maze) -> bool:
        x, y = self.get_center()
        current_cell = maze.get_cell(x, y)
        if current_cell == maze.victory_cell:
            return True
        current_cell.request_update()
        dx, dy = vector.x, vector.y

        target_x = min(maze.width - 1, x + dx * self.speed)
        target_y = min(maze.width - 1, y + dy * self.speed)

        target_x_cell = maze.get_cell(target_x, y)
        target_y_cell = maze.get_cell(x, target_y)

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
        return False

