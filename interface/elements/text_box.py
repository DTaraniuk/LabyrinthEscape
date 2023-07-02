from common import constants
from .ui_element import UiElement
import pygame
import pyperclip


class TextBox(UiElement):
    def __init__(self,
                 name: str,
                 area: pygame.Rect = None,
                 color: tuple[int, int, int] = constants.WHITE,
                 text: str = '',
                 text_color: tuple[int, int, int] = constants.BLACK,
                 level: int = 0,
                 active: bool = False,
                 clear_init_text_on_select: bool = False
                 ):
        super().__init__(name=name,
                         area=area,
                         color=color,
                         level=level,
                         active=active)
        self.text = text
        self.text_color = text_color
        self.clear_init_text_on_select = clear_init_text_on_select

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.area)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, self.text_color)
        surface.blit(text_surface, self.area)

    def paste(self):
        self.text += pyperclip.paste()
