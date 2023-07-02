import pygame
from typing import Optional
from game_logic import GameState, Maze, CoordPair, LePlayer, LeMinotaur
from graphics import Renderer
from common import constants, helper
from .ui import Ui


class SinglePlayerUi(Ui):
    def __init__(self):
        super().__init__()
        maze = Maze(constants.ROWS, constants.WIDTH)
        maze.generate_labyrinth()

        center = (constants.ROWS // 2 + 0.5) * maze.cell_width
        player_start = CoordPair(center, center)
        self._player_name = 'Mighty Mouse'
        self._player = LePlayer(player_start, (maze.cell_width / 2, maze.cell_width / 2), self._player_name)

        mino_start = maze.get_random_edge_cell().get_pos()
        mino_name = 'Billy'
        minotaur = LeMinotaur(pos=mino_start,
                              size=(maze.cell_width, maze.cell_width),
                              name=mino_name)

        self.gs = GameState(maze)
        self.gs.add_player(minotaur)
        self.gs.add_player(self._player)

        self._renderer: Optional[Renderer] = None

    def process_events(self, events: list[pygame.event.Event]):
        for event in events:
            self.process_event(event)
        move_direction = helper.input_movement()
        self._player.move_direction = move_direction
        self.gs.advance_timeline(1)

    def process_event(self, event: pygame.event.Event):
        pass

    def render(self, surface: pygame.Surface):
        if not self._renderer:
            self._renderer = Renderer(surface, self._player_name)

        self._renderer.render(self.gs)
