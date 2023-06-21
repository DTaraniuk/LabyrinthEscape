import pygame

from .image_storage import ImageStorage
from .surface_manager import SurfaceManager, SurfaceType
from pygame import Rect
from game_logic import GameState
from common import constants, helper


class Renderer:
    def __init__(self, win: pygame.Surface, player_name: str):
        surface_manager = SurfaceManager(win)
        surface_manager.init_surfaces()
        self._player_name: str = player_name
        self._surface_manager: SurfaceManager = surface_manager
        self._image_storage = ImageStorage()
        self._show_grid: bool = False

    def update_surfaces(self, gs: GameState):
        self._surface_manager.update_maze_surface(gs.maze)
        players_with_images = [(player, self._image_storage.get_or_add(player)) for player in gs.players.values()]
        self._surface_manager.update_play_surface(players_with_images)

    def render(self, gs: GameState):
        self.update_surfaces(gs)
        rect_list: list[pygame.Rect] = []
        player = gs.players[self._player_name]
        cells = gs.get_player_vision(player)
        for cell in cells:
            x, y = cell.get_pos()
            rect: Rect = Rect(x, y, cell.width, cell.width)
            rect_list.append(rect)
        self._surface_manager.render(rect_list=rect_list)

    def user_message(self, text: str, font_size: int):
        font_ = pygame.font.Font(None, font_size)
        self._surface_manager.update_opaque_surface(0.5)
        self._surface_manager.update_text_surface(text, font_)
        self._surface_manager.show_surface(SurfaceType.OPAQ)
        self._surface_manager.show_surface(SurfaceType.TEXT)
        self._surface_manager.render()
        helper.wait_for_input()
        self._surface_manager.hide_surface(SurfaceType.OPAQ)
        self._surface_manager.hide_surface(SurfaceType.TEXT)
        self._surface_manager.render()

    def toggle_grid(self):
        if self._show_grid:
            self._surface_manager.hide_surface(SurfaceType.GRID)
            self._show_grid = False
        else:
            self._surface_manager.show_surface(SurfaceType.GRID)
            self._show_grid = True

    def refresh(self, gs: GameState):
        gs.maze.request_full_update()
        self._surface_manager.update_maze_surface(gs.maze)
        self._surface_manager.clear_surface(SurfaceType.PLAY)

    def render_path(self, pathfinding_res, path_color):
        self._surface_manager.update_path_surface(pathfinding_res.path, path_color)
