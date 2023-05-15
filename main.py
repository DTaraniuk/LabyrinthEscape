import pygame

import game_state
import pathfinding
from pygame import Surface as pgs
from game_state import GameState, index_string
from surface_manager import SurfaceManager
from maze import Maze
from pathfinding import*
from constants import*
import event_handler
from player import Player
from minotaur import Minotaur
from coordpair import CoordPair

pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Labyrinth Escape")


def refresh(surface_manager, maze):
    maze.request_full_update()
    surface_manager.update_maze_surface(maze)
    surface_manager.clear_surface("path")


def reset(surface_manager: SurfaceManager, gs: GameState, player, minotaur) -> Maze:
    new_maze = Maze(ROWS, WIDTH)
    new_maze.generate_labyrinth()
    surface_manager.update_maze_surface(new_maze)

    center = (ROWS // 2 + 0.5) * new_maze.cell_width
    player_start = CoordPair(center, center)
    mino_start = new_maze.get_random_edge_cell().get_pos()

    player.set_pos(player_start)
    minotaur.set_pos(mino_start)
    surface_manager.update_play_surface([player, minotaur])
    gs.maze = new_maze
    return new_maze


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

    center = (ROWS // 2 + 0.5) * maze.cell_width
    player_start = CoordPair(center, center)
    player_img = pygame.image.load(f"{IMG_FOLDER}\\{PLAYER_IMG}")
    player = Player(player_start, (maze.cell_width/2, maze.cell_width/2), player_img)

    mino_start = maze.get_random_edge_cell().get_pos()
    minotaur_img = pygame.image.load(f"{IMG_FOLDER}\\{MINOTAUR_IMG}")
    minotaur = Minotaur(mino_start, (maze.cell_width, maze.cell_width), minotaur_img)

    surface_manager.update_play_surface([player, minotaur], maze)

    clock = pygame.time.Clock()

    gs = GameState(player, minotaur, maze)

    run = True
    event_handler.user_message(surface_manager, "Privet. Click to start", FONT_SIZE)
    surface_manager.render()
    while run:
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                run = False
                break

            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_a:
                    event_handler.handle_pathfinding_call(surface_manager, maze, pathfinding.astar, RED)
                elif event_.key == pygame.K_d:
                    event_handler.handle_pathfinding_call(surface_manager, maze, pathfinding.dfs_path, BLUE)
                elif event_.key == pygame.K_b:
                    event_handler.handle_pathfinding_call(surface_manager, maze, pathfinding.bfs_path, GREEN)
                elif event_.key == pygame.K_SPACE:
                    # maze.process_cells(lambda cell: setattr(cell, 'color', WHITE))
                    refresh(surface_manager, maze)
                elif event_.key == pygame.K_r:
                    maze = reset(surface_manager, gs, player, minotaur)
                elif event_.key == pygame.K_g:
                    surface_manager.toggle_grid_surface()
                    maze.request_full_update()

        # move player
        keys = pygame.key.get_pressed()
        player_move_vector = CoordPair()
        if keys[pygame.K_UP]:
            player_move_vector += CoordPair(0, -1)
        if keys[pygame.K_DOWN]:
            player_move_vector += CoordPair(0, 1)
        if keys[pygame.K_LEFT]:
            player_move_vector += CoordPair(-1, 0)
        if keys[pygame.K_RIGHT]:
            player_move_vector += CoordPair(1, 0)
        player.move_direction = player_move_vector

        gs.advance_timeline(1)

        victory = gs.check_win_lose()
        if victory is not None:
            if victory:
                event_handler.user_message(surface_manager, f"You have escaped for the {game_state.index_string(gs.escapes)} time", FONT_SIZE)
                maze.randomize_victory_cell()
                refresh(surface_manager, maze)
            else:
                event_handler.user_message(surface_manager, f"You have been slain by the minotaur", FONT_SIZE)
                maze = reset(surface_manager, gs, player, minotaur)

        surface_manager.update_maze_surface(maze)
        surface_manager.update_play_surface([player, minotaur], maze)

        clock.tick(FPS)
        surface_manager.render(maze=maze)

    pygame.quit()


main(WIN)
