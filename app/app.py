import pygame
from interface import RunMode, Ui, MpLobbyUi, MpGameUi
from common import constants
from typing import Callable


class LeApp:
    def __init__(self, win: pygame.Surface):
        self.uis: dict[RunMode, Ui] = {}
        self.run_mode_stack: list[RunMode] = [RunMode.Menu]
        self.active_ui: Ui = None
        self.main_surface: pygame.Surface = win
        self._run: bool = False

        self._ui_transition_map: dict[tuple[RunMode, RunMode], Callable[[], None]] = {
            (RunMode.MpLobby, RunMode.MpGame): self._from_mp_lobby_to_mp_game
        }

    def add_ui(self, ui: Ui, mode: RunMode):
        self.uis[mode] = ui

    def run(self):
        self._run = True
        self.active_ui = self.uis[self.run_mode_stack[-1]]
        clock = pygame.time.Clock()

        while self._run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._run = False

            self.active_ui.process_events(events)

            self.ui_transition()

            self.active_ui.render(self.main_surface)
            pygame.display.flip()
            clock.tick(constants.FPS)

        pygame.quit()

    # region ui transitions

    def ui_transition(self):
        if self.active_ui.switch_mode:
            current_run_mode = self.run_mode_stack[-1]
            mode_pair: tuple[RunMode, RunMode] = (current_run_mode, self.active_ui.switch_mode)
            if mode_pair in self._ui_transition_map:
                action = self._ui_transition_map.get(mode_pair)
            else:
                action = self._from_any_to_any
            action()

    def _from_any_to_any(self):
        next_mode = self.active_ui.switch_mode
        self.active_ui.switch_mode = None
        self.active_ui.reset()
        if next_mode == RunMode.Prev:
            if len(self.run_mode_stack) > 1:
                self.run_mode_stack.pop()
        else:
            self.run_mode_stack.append(next_mode)
        self.active_ui = self.uis[self.run_mode_stack[-1]]

    def _from_mp_lobby_to_mp_game(self):
        lobby_ui = self.active_ui
        mp_game_ui = self.uis[RunMode.MpGame]
        if not (isinstance(lobby_ui, MpLobbyUi) and isinstance(mp_game_ui, MpGameUi)):
            print(f'Error occurred during transition from lobby to game')
            return

        mp_game_ui.gs = lobby_ui.gs
        mp_game_ui.client = lobby_ui.client
        mp_game_ui.player_name = lobby_ui.player_name
        self._from_any_to_any()

    # endregion
