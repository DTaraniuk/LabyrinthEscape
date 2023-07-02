from .ui import Ui, RunMode
from .elements import TextBox, Button, ListBox
from common import constants
from typing import Optional, Callable, Any
from networking import Client, SockMessage, MsgType
from game_logic import GameState
import pygame

ELEMENT_WIDTH_GAP = constants.WIDTH / 3
ELEMENT_HEIGHT_GAP = constants.WIDTH / 6
ELEMENT_WIDTH = constants.WIDTH - ELEMENT_WIDTH_GAP * 2
ELEMENT_HEIGHT = constants.WIDTH / 12
ELEMENT_GAP = constants.WIDTH / 20

IP_TB_INIT_TEXT = 'Enter host server(DIMAS) IPv4'
IP_TB_NAME = 'name_tb'
NAME_TB_INIT_TEXT = 'Enter your name'
NAME_TB_NAME = 'name_btn'
CONNECT_BUTTON_NAME = 'conn_btn'
PLAYER_LB_NAME = 'player_lb'
READY_BTN_NAME = 'rdy_btn'


def get_area_rect(pos: int):
    return pygame.Rect(ELEMENT_WIDTH_GAP,
                       ELEMENT_HEIGHT_GAP + ELEMENT_HEIGHT * pos,
                       ELEMENT_WIDTH,
                       ELEMENT_HEIGHT)


class MpLobbyUi(Ui):
    def __init__(self):
        super().__init__()

        self._btn_action_map: dict[str, Callable] = {
            CONNECT_BUTTON_NAME: self.on_conn_btn_press,
            READY_BTN_NAME: self.on_ready_btn_press
        }

        self._msg_action_map: dict[MsgType, Callable[[SockMessage], Any]] = {
            MsgType.CONN: self.update_player_status,
            MsgType.RDY: self.update_player_status,
            MsgType.START: self.start_game,
            MsgType.LOBBY_INIT: self.init_lobby
        }

        self.hotkeys.update({pygame.K_v: self.paste})
        # region elements
        self._name_text_box = TextBox(name=NAME_TB_NAME,
                                      area=get_area_rect(0),
                                      color=constants.BLUE,
                                      text=NAME_TB_INIT_TEXT,
                                      text_color=constants.ORANGE,
                                      active=True,
                                      clear_init_text_on_select=True)
        self.elements.append(self._name_text_box)
        self._ip_text_box = TextBox(name=IP_TB_NAME,
                                    area=get_area_rect(1),
                                    color=constants.BLUE,
                                    text=IP_TB_INIT_TEXT,
                                    text_color=constants.ORANGE,
                                    active=True,
                                    clear_init_text_on_select=True)
        self.elements.append(self._ip_text_box)
        self._connect_btn = Button(name=CONNECT_BUTTON_NAME,
                                   area=get_area_rect(2),
                                   color=constants.RED,
                                   label='Connect',
                                   label_color=constants.BLUE,
                                   active=True)
        self.elements.append(self._connect_btn)
        self._tb_input: Optional[TextBox] = None
        # client-server
        self._ready_button = Button(name=READY_BTN_NAME,
                                    area=get_area_rect(0),
                                    color=constants.RED,
                                    label='Ready',
                                    label_color=constants.BLUE,
                                    active=False)
        self.elements.append(self._ready_button)
        self._player_list_box = ListBox(name=PLAYER_LB_NAME,
                                        area=get_area_rect(1),
                                        color=constants.LIGHT_BLUE,
                                        item_color=constants.BLACK,
                                        label='Currently connected players',
                                        label_color=constants.ORANGE,
                                        active=False)
        self.elements.append(self._player_list_box)
        # endregion
        self._player_ready_map: dict[str, bool] = {}
        self.client: Optional[Client] = Client()
        self.gs: Optional[GameState] = None
        self.player_name: Optional[str] = None

    def process_events(self, events: list[pygame.event.Event]):
        client_messages = self.client.fetch_messages()
        for message in client_messages:
            self.process_server_message(message)
        super().process_events(events)

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            element = self.get_affected_element(event)
            self._tb_input = None
            if isinstance(element, TextBox):
                self._tb_input = element
                if element.clear_init_text_on_select:
                    element.text = ''
            elif isinstance(element, Button):
                action = self._btn_action_map.get(element.name)
                if not action:
                    self.user_info(f"Element not in action map: {element.name}")
                else:
                    action()

        elif event.type == pygame.KEYDOWN:
            # hotkeys
            if event.key in self.hotkeys:
                if self.hotkeys[event.key]():
                    return
            # input
            if not self._tb_input:
                return
            else:
                tb = self._tb_input
                if event.key == pygame.K_RETURN:
                    self._tb_input = None
                elif event.key == pygame.K_BACKSPACE:
                    tb.text = tb.text[:-1]
                else:
                    tb.text += event.unicode

    def paste(self) -> bool:
        if self._tb_input and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self._tb_input.paste()
            return True
        return False

    # region button actions

    def on_conn_btn_press(self):
        success = self.client.try_connect(self._ip_text_box.text)
        if not success:
            self._ip_text_box.text_color = constants.RED
            return
        self._ip_text_box.active = False
        self._name_text_box.active = False
        self._connect_btn.active = False
        self._player_list_box.active = True
        self._ready_button.active = True
        self.client.send_message(MsgType.CONN, self._name_text_box.text)

    def on_ready_btn_press(self):
        self.client.send_message(MsgType.RDY, None)

    # endregion

    # region msg actions

    def process_server_message(self, msg: SockMessage):
        if msg.msg_type in self._msg_action_map:
            self._msg_action_map[msg.msg_type](msg)

    def update_player_status(self, msg: SockMessage) -> None:
        if not isinstance(msg.msg_content, str):
            self.user_info('Bad response from server on update player status.')
            return
        player_name = msg.msg_content

        if msg.msg_type == MsgType.CONN:
            self._player_ready_map[player_name] = False
            listbox_entry = f'{player_name}:{self.player_ready_str(player_name)}'
            self._player_list_box.add_item(listbox_entry)

        elif msg.msg_type == MsgType.RDY:
            self._player_ready_map[player_name] = not self._player_ready_map[player_name]
            listbox_entry_index = list(self._player_ready_map.keys()).index(player_name)
            listbox_entry = f'{player_name}:{self.player_ready_str(player_name)}'
            self._player_list_box.update_item(listbox_entry, listbox_entry_index)

    def player_ready_str(self, name: str) -> str:
        if name not in self._player_ready_map:
            self.user_info('Error in player ready str')
            return ':('
        return 'Ready' if self._player_ready_map[name] else 'Not ready'

    def start_game(self, msg: SockMessage):
        self.switch_mode = RunMode.MpGame
        # receive initial game state
        self.gs = msg.msg_content

    def init_lobby(self, msg: SockMessage):
        player_name, player_ready_map = msg.msg_content
        self.player_name = player_name
        self._player_ready_map = player_ready_map

    # endregion
