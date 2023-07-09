import pygame
from game_logic import Cell, LePlayer, Wall


class SurfaceUpdateData:
    def __init__(self,
                 cells_to_update: list[Cell] = None,
                 walls_to_update: list[Wall] = None,
                 path: list[Cell] = None,
                 path_color: tuple[int, int, int] = None,
                 text: str = None,
                 font: pygame.font.Font = None,
                 players_with_images: list[tuple[LePlayer, pygame.Surface]] = None,
                 opacity: float = None,
                 shade_color: tuple[int, int, int] = None):
        # maze
        self.cells_to_update = cells_to_update
        self.walls_to_update = walls_to_update
        # path
        self.path = path
        self.path_color = path_color
        # text
        self.text = text
        self.font = font
        # play
        self.players_with_images = players_with_images
        # opaque
        self.opacity = opacity
        self.shade_color = shade_color

    def get_rect_list(self) -> list[pygame.Rect]:
        rect_list: list[pygame.Rect] = []
        for cell in self.cells_to_update:
            x, y = cell.get_pos()
            rect: pygame.Rect = pygame.Rect(x, y, cell.width, cell.width)
            rect_list.append(rect)
        return rect_list
