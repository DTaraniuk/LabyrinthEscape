from abc import ABC, abstractmethod
from typing import Callable
from interface.elements.ui_element import UiElement
from typing import Optional
from .run_mode import RunMode
from .elements.text_box import TextBox
from common import constants
import pygame

INFO_BOX_WIDTH = 200
INFO_BOX_HEIGHT = 50


class Ui(ABC):
    def __init__(self):
        self.elements: list[UiElement] = []
        self.hotkeys: dict[int, Callable[[], bool]] = {
            pygame.K_ESCAPE: self.back_hotkey
        }
        self.switch_mode: Optional[RunMode] = None

        # region common elements
        self._info_text_box = TextBox(name='info_tb',
                                      area=pygame.Rect(constants.WIDTH - INFO_BOX_WIDTH,
                                                       constants.HEIGHT - INFO_BOX_HEIGHT,
                                                       INFO_BOX_WIDTH, INFO_BOX_HEIGHT),
                                      color=constants.BLUE,
                                      text_color=constants.ORANGE,
                                      active=False)
        self.elements.append(self._info_text_box)
        # endregion

    def add_element(self, element: UiElement):
        self.elements.append(element)

    def process_events(self, events: list[pygame.event.Event]):
        for event in events:
            self.process_event(event)

    @abstractmethod
    def process_event(self, event: pygame.event.Event):
        pass

    def get_affected_element(self, event: pygame.event.Event) -> Optional[UiElement]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()
            for element in (e for e in self.elements if e.active):
                if element.area.collidepoint(click_pos):
                    return element
        return None

    def render(self, surface: pygame.Surface):
        surface.fill(constants.GREY)
        for element in sorted(self.elements, key=lambda e: -e.level):
            if element.active:
                element.draw(surface)

    def user_info(self, text: str) -> None:
        self._info_text_box.active = True
        self._info_text_box.text = text

    def back_hotkey(self) -> bool:
        self.switch_mode = RunMode.Prev
        return True


