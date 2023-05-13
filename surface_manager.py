import math
import pygame
from constants import*
from pygame import Surface as pgs
from typing import Tuple
from cell import Cell
from maze import Maze
from player import Player


class SurfaceManager:
    def __init__(self, main_surface: pgs):
        self.show_grid = False
        self.surfaces: dict[str, pgs] = {SURFACE_MAIN: main_surface}

    def create_surface(self, name: str, size: Tuple[int, int]):
        self.surfaces[name] = pgs(size, pygame.SRCALPHA)

    def get_surface(self, name: str) -> pgs:
        return self.surfaces[name]

    def clear_surface(self, name: str):
        surface_ = self.surfaces.get(name, None)
        if surface_ is not None:
            surface_.fill(TRANSPARENT)

    def render_maze(self, maze: Maze):
        rects_to_update = []

        def get_rect(c: Cell, rects: list[pygame.Rect]):
            if not c.is_up_to_date:
                rects.append(pygame.Rect(c.index_in_col * c.width, c.index_in_row * c.width, c.width, c.width))

        maze.process_cells(lambda c: get_rect(c, rects_to_update))

        self.render(rects_to_update)
        for cell in maze.get_cells():
            cell.mark_updated()

    def render(self, rect_list: list[pygame.Rect] = None):
        main_surface: pgs = self.surfaces.get(SURFACE_MAIN)
        main_surface.fill(BLACK)

        if rect_list is not None:
            for rect in rect_list:
                for surface in self.surfaces.values():
                    main_surface.blit(surface, rect, area=rect)
            pygame.display.update(rect_list)
        else:
            dest = (0, 0)
            for surface in self.surfaces.values():
                main_surface.blit(surface, dest)
            pygame.display.flip()

    def update_path_surface(self, path: list[Cell], path_color) -> bool:
        path_surface = self.surfaces[SURFACE_PATH]
        if path.__len__() == 0:
            return False
        width = WIDTH / ROWS
        points: list[Tuple[int, int]] = []
        for cell in path:
            cell.request_update()
            points.append((cell.index_in_row * width + width / 2, cell.index_in_col * width + width / 2))
        pygame.draw.lines(path_surface, path_color, closed=False, points=points, width=WALL_WIDTH)

    def update_maze_surface(self, maze: Maze) -> None:
        maze_surface: pygame.Surface = self.surfaces[SURFACE_MAZE]
        for cell in maze.get_cells():
            cell.draw(maze_surface)

    def toggle_grid_surface(self):
        grid_surface: pygame.Surface = self.surfaces[SURFACE_GRID]
        if self.show_grid:
            cell_width = WIDTH / ROWS
            for i in range(ROWS):
                pygame.draw.line(grid_surface, GREY, (0, i * cell_width), (WIDTH, i * cell_width))

            for i in range(ROWS):
                pygame.draw.line(grid_surface, GREY, (i * cell_width, 0), (i * cell_width, WIDTH))
        else:
            self.clear_surface(SURFACE_GRID)
        self.show_grid = not self.show_grid

    def update_text_surface(self, text: str, font_: pygame.font.Font):
        text_surface = create_text_frame(text, font_, text_color=PINK, frame_color=BLACK, padding=int(font_.get_height()/2), aspect_ratio=(3, 2))
        self.surfaces[SURFACE_TEXT] = text_surface

    def update_play_surface(self, players: list[Player]):
        play_surface = self.surfaces[SURFACE_PLAY]
        play_surface.fill(TRANSPARENT)
        for player in players:
            play_surface.blit(player.image, player.get_pos().to_tuple())

    def show_text(self):
        text_surface: pgs = self.surfaces[SURFACE_TEXT]
        main_surface: pgs = self.surfaces.get(SURFACE_MAIN)
        width = text_surface.get_rect().width
        height = text_surface.get_rect().height
        x_coord = (WIDTH - width)/2
        y_coord = (WIDTH - height)/2
        shade_surface: pgs = pgs(main_surface.get_size(), pygame.SRCALPHA)
        shade_surface.fill(GREY + (128,))
        main_surface.blit(shade_surface, (0, 0))
        main_surface.blit(text_surface, (x_coord, y_coord))
        pygame.display.flip()


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        line_width, _ = font.size(' '.join(current_line))

        if line_width > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def create_text_frame(text: str, font: pygame.font.Font, text_color: Tuple[int, int, int], frame_color: Tuple[int, int, int], padding: int, aspect_ratio: Tuple[int, int]) -> pygame.Surface:
    line_surface = font.render(text, True, text_color) # create a surface to get total len
    length = line_surface.get_width()
    height = font.get_height()
    desired_width = int(math.sqrt(height * aspect_ratio[0] / aspect_ratio[1] * length))

    # Calculate lines with the desired width.
    lines = wrap_text(text, font, desired_width)
    line_surfaces = [font.render(line, True, text_color) for line in lines]
    max_line_width = max(line_surface.get_width() for line_surface in line_surfaces)

    frame_width = max_line_width + 2 * padding
    frame_height = height * lines.__len__() + 2 * padding

    frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
    frame_surface.fill(WHITE)

    pygame.draw.rect(frame_surface, frame_color, (0, 0, frame_width, frame_height), padding)

    for i, line_surface in enumerate(line_surfaces):
        x = padding
        y = padding + i * height
        frame_surface.blit(line_surface, (x, y))

    return frame_surface

