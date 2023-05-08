import pathfinding
from pygame import Surface as pgs
from surface_manager import SurfaceManager
from maze import Maze
from pathfinding import*
from constants import*
import event_handler
from player import Player


pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Labyrinth Escape")


def init_surfaces(win: pgs) -> SurfaceManager:
    scr_size = (WIDTH, WIDTH)
    surface_manager: SurfaceManager = SurfaceManager(win)
    surface_manager.create_surface(SURFACE_MAZE, scr_size)
    surface_manager.create_surface(SURFACE_GRID, scr_size)
    surface_manager.create_surface(SURFACE_PATH, scr_size)
    surface_manager.create_surface(SURFACE_PLAY, scr_size)
    return surface_manager


def main(win: pgs) -> None:
    surface_manager = init_surfaces(win)

    maze = Maze(ROWS, WIDTH)
    maze.generate_labyrinth()
    surface_manager.update_maze_surface(maze)
    surface_manager.render()

    coord = ROWS // 2 + 0.5 * maze.cell_width
    player = Player(coord, coord, (maze.cell_width/2, maze.cell_width/2))

    event_handler.user_message(surface_manager, "Тут могла быть Ваша реклама", 30, (0.0, 0.0))

    run = True
    while run:

        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                run = False

            elif event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_a:
                    event_handler.handle_pathfinding_call(surface_manager, maze, pathfinding.astar, RED, ORANGE)
                elif event_.key == pygame.K_d:
                    event_handler.handle_pathfinding_call(surface_manager, maze, pathfinding.dfs_path, BLUE, LIGHT_BLUE)
                elif event_.key == pygame.K_b:
                    event_handler.handle_pathfinding_call(surface_manager, maze, pathfinding.bfs_path, GREEN, PINK)
                elif event_.key == pygame.K_SPACE:
                    maze.process_cells(lambda cell: setattr(cell, 'color', WHITE))
                    maze.request_full_update()
                    surface_manager.update_maze_surface(maze)
                    surface_manager.clear_surface("path")
                elif event_.key == pygame.K_r:
                    maze = Maze(ROWS, WIDTH)
                    maze.generate_labyrinth()
                    surface_manager.update_maze_surface(maze)
                elif event_.key == pygame.K_g:
                    surface_manager.toggle_grid_surface()
                    maze.request_full_update()
                elif event_.key == pygame.K_UP:
                    player.move(0, -1)
                elif event_.key == pygame.K_DOWN:
                    player.move(0, 1)
                elif event_.key == pygame.K_LEFT:
                    player.move(-1, 0)
                elif event_.key == pygame.K_RIGHT:
                    player.move(1, 0)

            surface_manager.render()

    pygame.quit()


main(WIN)
