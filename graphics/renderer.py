import pygame

from .image_storage import ImageStorage
from .surface_manager import SurfaceManager
from pygame import Rect
from game_logic import GameState
from common import constants, helper


class Renderer:
    def __init__(self, win: pygame.Surface, player_id: int):
        surface_manager = SurfaceManager(win)
        surface_manager.init_surfaces()
        self._player_id: int = player_id
        self._surface_manager: SurfaceManager = surface_manager
        self._image_storage = ImageStorage()

    def update_surfaces(self, gs: GameState):
        self._surface_manager.update_maze_surface(gs.maze)
        players_with_images = [(player, self._image_storage.get_or_add(player)) for player in gs.players]
        self._surface_manager.update_play_surface(players_with_images)

    def render(self, gs: GameState):
        self.update_surfaces(gs)
        rect_list: list[pygame.Rect] = []
        player = gs.players[self._player_id]
        cells = gs.get_player_vision(player)
        for cell in cells:
            x, y = cell.get_pos()
            rect: Rect = Rect(x, y, cell.width, cell.width)
            rect_list.append(rect)
        self._surface_manager.render(rect_list=rect_list)

    def user_message(self, text: str, font_size: int):
        font_ = pygame.font.Font(None, font_size)
        self._surface_manager.update_text_surface(text, font_)
        self._surface_manager.show_text()
        helper.wait_for_input()
        self._surface_manager.clear_surface(constants.SURFACE_TEXT)
        self._surface_manager.render()

    def toggle_grid(self):
        self._surface_manager.toggle_grid_surface()

    def refresh(self, gs: GameState):
        gs.maze.request_full_update()
        self._surface_manager.update_maze_surface(gs.maze)
        self._surface_manager.clear_surface(constants.SURFACE_PATH)

    def render_path(self, pathfinding_res, path_color):
        self._surface_manager.update_path_surface(pathfinding_res.path, path_color)
