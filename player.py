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
        self.is_alive = True
        self.move_direction: CoordPair = CoordPair()
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
