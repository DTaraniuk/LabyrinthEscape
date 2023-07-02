from .ui_element import UiElement
from typing import Optional
import pygame


class ListBox(UiElement):
    def __init__(self,
                 name: str,
                 area: pygame.Rect,
                 color: tuple[int, int, int],
                 item_color: tuple[int, int, int],
                 label: str,
                 label_color: tuple[int, int, int],
                 level: int = 0,
                 active: bool = False):
        super().__init__(name, area, color, level, active)
        self.items: list[str] = []
        self.item_color: tuple[int, int, int] = item_color
        self.label: str = label
        self.label_color: tuple[int, int, int] = label_color
        self.selected_item: Optional[str] = None
        self.font: pygame.font.Font = pygame.font.Font(None, 24)  # specify the font for the listbox items

    def add_item(self, item: str) -> None:
        self.items.append(item)

    def update_item(self, item: str, pos: int):
        self.items[pos] = item

    def remove_item(self, item: str) -> None:
        if item in self.items:
            self.items.remove(item)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.area)

        label_text = self.font.render(self.label, True, self.label_color)
        label_pos = (self.area.x + (self.area.width - label_text.get_width()) // 2, self.area.y)
        surface.blit(label_text, label_pos)

        for i, item in enumerate(self.items):
            text = self.font.render(item, True, self.item_color)
            surface.blit(text, (self.area.x, self.area.y + label_text.get_height() + i * text.get_height()))

    def update_selected_item(self, mouse_pos: tuple[int, int]) -> None:
        if self.area.collidepoint(mouse_pos):
            index = (mouse_pos[1] - self.area.y) // self.font.get_height()
            if index < len(self.items):
                self.selected_item = self.items[index]

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.update_selected_item(pygame.mouse.get_pos())

