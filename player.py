from typing import Tuple
import pygame


class Player:
    def __init__(self, x: int, y: int, size: Tuple[int, int], img: pygame.image = None):
        self.x = x
        self.y = y
        self.size = size
        if img is not None:
            player_surface = img.convert_alpha()
            resized_player_surface = pygame.transform.scale(player_surface, self.size)
            self.image = resized_player_surface
        self.image = pygame.Surface(size, pygame.SRCALPHA)

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
