from abc import ABC, abstractmethod
from typing import Callable
from interface.elements.ui_element import UiElement
from typing import Optional
from .run_mode import RunMode
from .elements.text_box import TextBox
from common import constants
import pygame

INFO_BOX_NAME = 'info_tb'
INFO_BOX_WIDTH = 200
INFO_BOX_HEIGHT = 50


class Ui(ABC):
    def __init__(self):
        self.elements: list[UiElement] = []
        self._element_name_action_map: dict[str, Callable[[UiElement], None]] = {
            INFO_BOX_NAME: lambda el: setattr(el, 'active', False)
        }
        self._element_type_action_map: dict[type, Callable[[UiElement], None]] = {
            TextBox: self.on_text_box_click
        }
        self.hotkeys: dict[int, Callable[[], bool]] = {
            pygame.K_ESCAPE: self.back_hotkey
        }
        self.switch_mode: Optional[RunMode] = None
        self._tb_input: Optional[TextBox] = None

        # region common elements
        self._info_text_box = TextBox(name=INFO_BOX_NAME,
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

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.process_mousebuttondown_event(event)
        elif event.type == pygame.KEYDOWN:
            self.process_keydown_event(event)

    def process_keydown_event(self, event: pygame.event.Event):
        # hotkeys
        if event.key in self.hotkeys:
            success = self.hotkeys[event.key]()
            if success:
                return
        # input
        if not self._tb_input:
            return
        else:
            self.process_text_input(event)

    def process_mousebuttondown_event(self, event: pygame.event.Event):
        element = self.get_affected_element(event)
        self._tb_input = None
        if not element:
            return

        if type(element) in self._element_type_action_map:
            self._element_type_action_map[type(element)](element)

        if element.name in self._element_name_action_map:
            self._element_name_action_map[element.name](element)

    def process_text_input(self, event):
        tb = self._tb_input
        if event.key == pygame.K_RETURN:
            self._tb_input = None
        elif event.key == pygame.K_BACKSPACE:
            tb.text = tb.text[:-1]
        else:
            tb.text += event.unicode

    @abstractmethod
    def reset(self):
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

    def on_text_box_click(self, element: UiElement):
        if not isinstance(element, TextBox):
            self.user_info(f'Error in event processing: {element.name} not a text box')
            return
        self._tb_input = element
        if element.clear_text_on_select:
            element.text = ''
            element.clear_text_on_select = False

    def user_info(self, text: str) -> None:
        self._info_text_box.active = True
        self._info_text_box.text = text

    def back_hotkey(self) -> bool:
        self.switch_mode = RunMode.Prev
        return True


