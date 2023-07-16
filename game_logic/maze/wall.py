import enum
import pygame
from common import constants
from game_logic.material_object import IMaterialObject


class WallType(enum.Enum):
    Solid = 0


wall_type_to_color_map: dict[WallType, tuple[int, int, int]] = {
    WallType.Solid: constants.BLACK
}


class Wall(IMaterialObject):
    def __init__(self,
                 rect: pygame.Rect,
                 wall_type: WallType = WallType.Solid
                 ):
        self.color: tuple[int, int, int] = wall_type_to_color_map[wall_type]
        self._wall_type: WallType = wall_type
        self.area: pygame.Rect = rect
        self.is_updated: bool = False

    def get_area(self):
        return self.area

    def populate(self, other: 'Wall'):
        self.__init__(other.area, other.wall_type)

    @property
    def wall_type(self):
        return self._wall_type

    @wall_type.setter
    def wall_type(self, value: WallType):
        self.color = wall_type_to_color_map[value]
        self._wall_type = value
        self.is_updated = False
