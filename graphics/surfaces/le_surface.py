import pygame
import enum
from typing import Union, Optional
from .surface_update_data import SurfaceUpdateData
from abc import ABC, abstractmethod
from common import constants
from game_logic import CoordPair


class SurfaceType(enum.Enum):
    MAIN = 'main'
    CELL = 'cell'
    WALL = 'wall'
    GRID = 'grid'
    PATH = 'path'
    TEXT = 'text'
    PLAY = 'play'
    OPAQ = 'opaque'


class LeSurface(ABC):
    def __init__(self, surface: pygame.Surface, is_rendered=False):
        self._type = None
        self.is_rendered = is_rendered
        self._surface: pygame.Surface = surface

    @abstractmethod
    def update(self, upd_data: SurfaceUpdateData):
        pass

    def clear(self):
        self._surface.fill(constants.TRANSPARENT)

    def get_pgs(self):
        return self._surface

    def blit(self,
             source: 'LeSurface',
             dest: Union[CoordPair, tuple[float, float], pygame.Rect],
             area: Optional[pygame.Rect] = None,
             special_flags: int = 0):
        self._surface.blit(source.get_pgs(), dest, area, special_flags)

