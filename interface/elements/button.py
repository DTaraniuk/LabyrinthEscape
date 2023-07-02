from common import constants
from .ui_element import UiElement
import pygame


class Button(UiElement):
    def __init__(self,
                 name: str,
                 area: pygame.Rect,
                 label: str,
                 label_color: tuple[int, int, int],
                 color: tuple[int, int, int],
                 font_name: str = 'freesansbold.ttf',
                 font_size: int = constants.WIDTH//40,
                 level: int = 0,
                 active: bool = False):
        super().__init__(name=name,
                         area=area,
                         color=color,
                         level=level,
                         active=active)
        self.label: str = label
        self.label_color = label_color
        self.font = pygame.font.Font(font_name, font_size)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.area)

        # Create a surface with the rendered label
        label_surface = self.font.render(self.label, True, self.label_color)

        # Calculate the position where this surface should be blitted
        # in order to be centered in the button area
        label_rect = label_surface.get_rect(center=self.area.center)

        # Blit the label surface onto the screen
        screen.blit(label_surface, label_rect)
