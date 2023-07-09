import enum
import pygame
from common import helper, constants


class WallType(enum.Enum):
    Solid = 0


wall_type_to_color_map: dict[WallType, tuple[int, int, int]] = {
    WallType.Solid: constants.BLACK
}


class Wall:
    def __init__(self,
                 rect: pygame.Rect,
                 wall_type: WallType = WallType.Solid
                 ):
        self.color: tuple[int, int, int] = wall_type_to_color_map[wall_type]
        self.type: WallType = wall_type
        self.area: pygame.Rect = rect
        self.requires_update: bool = True

    def collide_circle(self, circle_center, circle_radius):
        rect = self.area
        return helper.collide_rect_circle(rect, circle_center, circle_radius)

    def populate(self, other: 'Wall'):
        self.__init__(other.area, other.type)
