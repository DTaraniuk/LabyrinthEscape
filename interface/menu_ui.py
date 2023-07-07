from .ui import Ui, UiElement
from .elements.button import Button
from .run_mode import RunMode
from common import constants
from typing import Optional, Callable
import pygame

BTN_COLOR = constants.LIGHT_BLUE
BTN_WIDTH_GAP = constants.WIDTH / 3
BTN_HEIGHT_GAP = constants.WIDTH / 6
BTN_WIDTH = constants.WIDTH - BTN_WIDTH_GAP * 2
BTN_HEIGHT = constants.WIDTH / 12
BTN_GAP = constants.WIDTH / 20
SINGLE_PLAYER_BUTTON_NAME = 'Single Player'
MULTI_PLAYER_BUTTON_NAME = 'MultiPlayer'


class MenuUi(Ui):
    def __init__(self):
        super().__init__()
        self._btn_action_map: dict[str, Callable] = {
            SINGLE_PLAYER_BUTTON_NAME: self.on_sp_btn_press,
            MULTI_PLAYER_BUTTON_NAME: self.on_mp_btn_press
        }
        btn_labels: list[str] = [SINGLE_PLAYER_BUTTON_NAME,
                                 MULTI_PLAYER_BUTTON_NAME]
        cnt = 0
        for btn_label in btn_labels:
            btn = Button(name=SINGLE_PLAYER_BUTTON_NAME,
                         area=pygame.Rect(BTN_WIDTH_GAP, BTN_HEIGHT_GAP + (BTN_GAP+BTN_HEIGHT)*cnt,
                                          BTN_WIDTH, BTN_HEIGHT),
                         label=btn_label,
                         label_color=constants.ORANGE,
                         color=BTN_COLOR,
                         active=True)
            cnt += 1
            self.add_element(btn)

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.hotkeys:
                self.hotkeys[event.key]()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            element = self.get_affected_element(event)
            if isinstance(element, Button):
                if element.label in self._btn_action_map.keys():
                    self._btn_action_map[element.label]()

    def reset(self):
        pass

    # region btn press methods

    def on_sp_btn_press(self):
        self.switch_mode = RunMode.SinglePlayer

    def on_mp_btn_press(self):
        self.switch_mode = RunMode.MpLobby

    # endregion

