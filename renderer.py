import pygame
from surface_manager import SurfaceManager
from pygame import Rect
from game_state import GameState
from player import Player


class Renderer:
    def __init__(self, surface_manager: SurfaceManager, player: Player):
        self._player = player
        self._surface_manager: SurfaceManager = surface_manager

    def update_surfaces(self, gs: GameState):
        self._surface_manager.update_maze_surface(gs.maze)
        self._surface_manager.update_play_surface(gs.players + [gs.minotaur], gs.maze)

    def render(self, gs: GameState):
        self.update_surfaces(gs)
        rect_list: list[pygame.Rect] = []
        cells = gs.get_player_vision(self._player)
        for cell in cells:
            x, y = cell.get_pos()
            rect: Rect = Rect(x, y, cell.width, cell.width)
            rect_list.append(rect)
        self._surface_manager.render(rect_list=rect_list)
