import math
import pygame
import enum

from common.constants import *
from pygame import Surface as pgs
from typing import Tuple
from game_logic import Cell, Maze, Player
from .drawer import draw_cell, draw_player
from common.helper import create_text_frame


class SurfaceType(enum.Enum):
    MAIN = 'main'
    MAZE = 'maze'
    GRID = 'grid'
    PATH = 'path'
    TEXT = 'text'
    PLAY = 'play'
    OPAQ = 'opaque'


class SurfaceManager:
    def __init__(self, main_surface: pgs):
        self._surfaces: dict[SurfaceType, pgs] = {SurfaceType.MAIN: main_surface}
        self._surface_visibility_map: dict[SurfaceType, bool] = {
            SurfaceType.MAIN: True,
            SurfaceType.MAZE: True,
            SurfaceType.GRID: False,
            SurfaceType.PATH: False,
            SurfaceType.TEXT: False,
            SurfaceType.OPAQ: False,
            SurfaceType.PLAY: True
        }

    def init_surfaces(self):
        scr_size = (WIDTH, WIDTH)
        # the order is crucial
        self.create_surface(SurfaceType.MAZE, scr_size)
        self.create_surface(SurfaceType.GRID, scr_size)
        self.create_surface(SurfaceType.PATH, scr_size)
        self.create_surface(SurfaceType.PLAY, scr_size)
        self.create_surface(SurfaceType.OPAQ, scr_size)
        self.create_surface(SurfaceType.TEXT, scr_size)

    def create_surface(self, surface_type: SurfaceType, size: Tuple[int, int]):
        self._surfaces[surface_type] = pgs(size, pygame.SRCALPHA)

    def get_surface(self, surface_type: SurfaceType) -> pgs:
        return self._surfaces[surface_type]

    def clear_surface(self, surface_type: SurfaceType):
        surface_ = self._surfaces.get(surface_type, None)
        if surface_ is not None:
            surface_.fill(TRANSPARENT)

    def render_maze(self, maze: Maze):
        rects_to_update = []

        def get_rect(c: Cell, rects: list[pygame.Rect]):
            if not c.is_updated:
                rects.append(pygame.Rect(c.index_in_col * c.width, c.index_in_row * c.width, c.width, c.width))

        maze.process_cells(lambda c: get_rect(c, rects_to_update))

        self.render(rects_to_update)
        for cell in maze.get_cells():
            cell.is_updated = True

    def render(self, rect_list: list[pygame.Rect] = None):
        main_surface: pgs = self._surfaces.get(SurfaceType.MAIN)
        main_surface.fill(GREY)

        if rect_list is not None:
            for surface_type, surface in self._surfaces.items():
                if not self._surface_visibility_map[surface_type]:
                    continue
                for rect in rect_list:
                    main_surface.blit(surface, rect, area=rect)
        else:
            for surface_type, surface in self._surfaces.items():
                if not self._surface_visibility_map[surface_type]:
                    continue
                dest = (0, 0)
                main_surface.blit(surface, dest)
        pygame.display.flip()

    # region update surfaces

    def update_path_surface(self, path: list[Cell], path_color) -> bool:
        path_surface = self._surfaces[SurfaceType.PATH]
        if path.__len__() == 0:
            return False
        width = WIDTH / ROWS
        points: list[Tuple[int, int]] = []
        for cell in path:
            cell.is_updated = False
            points.append((cell.index_in_row * width + width / 2, cell.index_in_col * width + width / 2))
        pygame.draw.lines(path_surface, path_color, closed=False, points=points, width=WALL_WIDTH)

    def update_maze_surface(self, maze: Maze) -> None:
        maze_surface: pygame.Surface = self._surfaces[SurfaceType.MAZE]
        for cell in maze.get_cells():
            draw_cell(cell, maze_surface)

    def toggle_grid_surface(self):
        grid_surface: pygame.Surface = self._surfaces[SurfaceType.GRID]
        if self._surface_visibility_map[SurfaceType.GRID]:
            cell_width = WIDTH / ROWS
            for i in range(ROWS):
                pygame.draw.line(grid_surface, GREY, (0, i * cell_width), (WIDTH, i * cell_width))

            for i in range(ROWS):
                pygame.draw.line(grid_surface, GREY, (i * cell_width, 0), (i * cell_width, WIDTH))
        else:
            self.clear_surface(SurfaceType.GRID)
        self._surface_visibility_map[SurfaceType.GRID] = not self._surface_visibility_map[SurfaceType.GRID]

    def update_text_surface(self, text: str, font_: pygame.font.Font):
        text_frame = create_text_frame(text,
                                       font_,
                                       text_color=PINK,
                                       frame_color=BLACK,
                                       padding=int(font_.get_height() / 2),
                                       aspect_ratio=(3, 2))
        width = text_frame.get_rect().width
        height = text_frame.get_rect().height
        x = (WIDTH - width) / 2
        y = (WIDTH - height) / 2
        text_surface = self._surfaces[SurfaceType.TEXT]
        text_surface.blit(text_frame, (x, y))

    def update_play_surface(self, players: list[tuple[Player, pygame.Surface]]):
        play_surface = self._surfaces[SurfaceType.PLAY]
        play_surface.fill(TRANSPARENT)
        for player, image in players:
            draw_player(player, image, play_surface)

    def update_opaque_surface(self, opacity: float):
        opacity_surface: pgs = self._surfaces.get(SurfaceType.OPAQ)
        opacity_surface.fill(GREY + (255 * (1 - opacity),))

    # endregion

    def show_surface(self, surface_type: SurfaceType):
        self._surface_visibility_map[surface_type] = True

    def hide_surface(self, surface_type: SurfaceType):
        self._surface_visibility_map[surface_type] = False
