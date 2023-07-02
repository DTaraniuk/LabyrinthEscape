from .ui import Ui, RunMode
from .elements import TextBox, Button, ListBox
from common import constants, helper
from typing import Optional, Callable, Any
from networking import Client, SockMessage, MsgType
from game_logic import GameState, GameStateChange
from graphics import Renderer
import pygame


class MpGameUi(Ui):
    def __init__(self):
        super().__init__()

        self._msg_action_map: dict[MsgType, Callable[[SockMessage], Any]] = {
            MsgType.GS_UPD: self.update_game_state,
            MsgType.MOVE: self.update_move_direction,
        }

        self.client: Optional[Client] = None
        self.gs: Optional[GameState] = None
        self.player_name: Optional[str] = None

        self._renderer: Optional[Renderer] = None

    def process_events(self, events: list[pygame.event.Event]):
        super().process_events(events)

        client_messages = self.client.fetch_messages()
        for message in client_messages:
            self.process_server_message(message)

        move_direction = helper.input_movement()
        player = self.gs.players.get(self.player_name)
        prev_move_direction = player.move_direction
        if move_direction != prev_move_direction:
            self.client.send_message(MsgType.MOVE, move_direction)
        self.gs.advance_timeline(1)

    def process_event(self, event: pygame.event.Event):
        pass

    def render(self, surface: pygame.Surface):
        if not self._renderer:
            self._renderer = Renderer(surface, self.player_name)
        self._renderer.render(self.gs)

    # region msg actions

    def process_server_message(self, msg: SockMessage):
        if msg.msg_type in self._msg_action_map:
            self._msg_action_map[msg.msg_type](msg)

    def update_game_state(self, msg: SockMessage):
        game_state_change: GameStateChange = msg.msg_content
        self.gs.apply_change(game_state_change)
        # print(f"recv update on time\t{self.client_gs.step} at {datetime.now().time()}")

    def update_move_direction(self, msg: SockMessage):
        player_name, new_direction, time = msg.msg_content
        self.gs.update_player_direction(player_name, new_direction, time)

    # endregion

