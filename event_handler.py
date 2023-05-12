from pathfinding import*
from typing import Callable
from surface_manager import SurfaceManager
from maze import Maze
import pygame


def wait_for_input():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return


def user_message(surface_manager: SurfaceManager, text: str, font_size: int):
    font_ = pygame.font.Font(None, font_size)
    surface_manager.update_text_surface(text, font_)
    surface_manager.show_text()
    wait_for_input()
    surface_manager.clear_surface(SURFACE_TEXT)
    surface_manager.render()


def read_endpoints(maze: Maze) -> Tuple[Cell, Cell]:
    click_num = 0
    width = WIDTH/ROWS
    start: Cell = None
    end: Cell = None
    while click_num < 2:
        click = pygame.event.wait()
        if click.type != pygame.MOUSEBUTTONDOWN:
            continue
        x, y = tuple(int(value // width) for value in click.pos)
        if click_num == 0:
            start = maze[x, y]
        else:
            end = maze[x, y]
        click_num += 1
    return start, end


def handle_pathfinding_call(surface_manager: SurfaceManager, maze, algo: Callable[[Cell, Cell], PathfindingRes], path_color: tuple[int, int, int], cell_color: tuple[int, int, int]):
    start, end = read_endpoints(maze)
    pathfinding_res = algo(start, end)
    # for cell in pathfinding_res.affected_nodes:
    #     cell.color = cell_color
    #     cell.request_update()
    surface_manager.update_path_surface(pathfinding_res.path, path_color)
    surface_manager.update_maze_surface(maze)



