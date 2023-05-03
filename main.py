import pathfinding
from pygame import Surface as pgs
from surface_manager import SurfaceManager
from maze import make_maze, generate_labyrinth
from pathfinding import*
from constants import*
import event_handler


pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Labyrinth Escape")


def refresh_cells(maze):
    for row in maze:
        for cell in row:
            cell.color = WHITE


def init_surfaces(win: pgs) -> SurfaceManager:
    scr_size = (WIDTH, WIDTH)
    surface_manager: SurfaceManager = SurfaceManager(win)
    surface_manager.create_surface(SURFACE_MAZE, scr_size)
    surface_manager.create_surface(SURFACE_GRID, scr_size)
    surface_manager.create_surface(SURFACE_PATH, scr_size)
    return surface_manager


def main(win: pgs) -> None:
    surface_manager = init_surfaces(win)

    maze = make_maze(ROWS, WIDTH)
    generate_labyrinth(maze, ROWS)
    surface_manager.update_maze_surface(maze)
    surface_manager.render()

    event_handler.user_message(surface_manager, "Тут могла быть Ваша реклама", 60, (0.0, 0.0))

    run = True
    while run:

        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                run = False

            elif event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_a:
                    event_handler.handle_pathfinding_call(surface_manager, maze, pathfinding.astar, RED, ORANGE)

                if event_.key == pygame.K_d:
                    event_handler.handle_pathfinding_call(surface_manager, maze, pathfinding.dfs_path, BLUE, LIGHT_BLUE)

                if event_.key == pygame.K_b:
                    event_handler.handle_pathfinding_call(surface_manager, maze, pathfinding.bfs_path, GREEN, PINK)

                if event_.key == pygame.K_SPACE:
                    refresh_cells(maze)
                    surface_manager.update_maze_surface(maze)
                    surface_manager.clear_surface("path")

                if event_.key == pygame.K_r:
                    maze = make_maze(ROWS, WIDTH)
                    generate_labyrinth(maze, ROWS)
                    surface_manager.update_maze_surface(maze)

                if event_.key == pygame.K_g:
                    surface_manager.toggle_grid_surface()
            surface_manager.render()

    pygame.quit()


main(WIN)
