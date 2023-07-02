from abc import ABC, abstractmethod
from typing import Callable
import pygame


class UiElement(ABC):
    def __init__(self,
                 name: str,
                 area: pygame.Rect,
                 color: tuple[int, int, int],
                 level: int = 0,
                 active: bool = False
                 ):
        self.name = name
        self.area = area
        self.color = color
        self.level = level
        self.active = active

    def __lt__(self, other: 'UiElement'):
        return self.level < other.level

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass
