import pygame
from typing import Optional
from game_logic import GameState, Maze, CoordPair, LePlayer, LeMinotaur, PlayerState
from graphics import Renderer
from common import constants, helper
from .ui import Ui


class SinglePlayerUi(Ui):
    def __init__(self):
        super().__init__()
        maze = Maze(constants.ROWS, constants.WIDTH)
        maze.generate_labyrinth()
        self.gs = GameState(maze)
        self._player: LePlayer = None

        self.init_sp_players()
        self._renderer: Optional[Renderer] = None

    def init_sp_players(self):
        maze = self.gs.maze
        center = (constants.ROWS // 2 + 0.5) * maze.cell_width
        player_start = CoordPair(center, center)
        self._player = LePlayer(player_start, (maze.cell_width / 2, maze.cell_width / 2), 'Mighty Mouse')

        mino_start = maze.get_random_edge_cell().get_pos()
        mino_name = 'Billy'
        minotaur = LeMinotaur(pos=mino_start,
                              size=(maze.cell_width, maze.cell_width),
                              name=mino_name)

        # minotaur should be added first
        self.gs.add_player(minotaur)
        self.gs.add_player(self._player)

    def process_events(self, events: list[pygame.event.Event]):
        for event in events:
            self.process_event(event)
        move_direction = helper.input_movement()
        self._player.move_direction = move_direction
        self.gs.advance_timeline(1)
        if self._player.state == PlayerState.DEAD:
            self.user_info('You have died')
            self.reset()
        elif self._player.state == PlayerState.ESCAPED:
            self.user_info('You have escaped')
            self.reset()

    def reset(self):
        maze = Maze(constants.ROWS, constants.WIDTH)
        maze.generate_labyrinth()
        self.gs = GameState(maze)
        self.init_sp_players()
        self._renderer = None

    def render(self, surface: pygame.Surface):
        if not self._renderer:
            self._renderer = Renderer(surface, self._player.name)

        self._renderer.render(self.gs)

        for element in sorted(self.elements, key=lambda e: -e.level):
            if element.active:
                element.draw(surface)
