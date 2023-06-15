import pygame
import game_state
import pathfinding
from pygame import Surface as pgs
from game_state import GameState, index_string
from maze import Maze
from pathfinding import*
from constants import*
import helper
from player import Player
from minotaur import Minotaur
from coordpair import CoordPair
from renderer import Renderer

pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Labyrinth Escape")


def main(win: pgs) -> None:
    player_renderer = Renderer(win, 1)  # 1 is the player index, 0 for minotaur

    maze = Maze(ROWS, WIDTH)
    maze.generate_labyrinth()

    center = (ROWS // 2 + 0.5) * maze.cell_width
    player_start = CoordPair(center, center)
    player = Player(player_start, (maze.cell_width/2, maze.cell_width/2), "Main-Kun")

    mino_start = maze.get_random_edge_cell().get_pos()

    minotaur = Minotaur(mino_start, (maze.cell_width, maze.cell_width))

    clock = pygame.time.Clock()

    gs = GameState(maze)
    gs.add_player(minotaur)
    gs.add_player(player)

    run = True
    player_renderer.user_message("Privet. Click to start", FONT_SIZE)
    while run:
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                run = False
                break

            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_a:
                    helper.handle_pathfinding_call(player_renderer, maze, pathfinding.astar, RED)
                elif event_.key == pygame.K_d:
                    helper.handle_pathfinding_call(player_renderer, maze, pathfinding.dfs_path, BLUE)
                elif event_.key == pygame.K_b:
                    helper.handle_pathfinding_call(player_renderer, maze, pathfinding.bfs_path, GREEN)
                elif event_.key == pygame.K_SPACE:
                    # maze.process_cells(lambda cell: setattr(cell, 'color', WHITE))
                    player_renderer.refresh(gs)
                elif event_.key == pygame.K_r:
                    gs.reset()
                elif event_.key == pygame.K_g:
                    player_renderer.toggle_grid()

        # move player
        player_move_vector = helper.input_movement()
        player.move_direction = player_move_vector

        gs.advance_timeline(1)

        victory = gs.check_win_lose()
        if victory is None:
            player_renderer.user_message(f"You have escaped for the {game_state.index_string(gs.escapes)} time", FONT_SIZE)
            maze.randomize_victory_cell()
            player_renderer.refresh(gs)
        else:
            for player, is_dead in victory.items():
                if is_dead:
                    player_renderer.user_message(f"You have been slain by the minotaur", FONT_SIZE)
                    gs.reset()

        clock.tick(FPS)
        player_renderer.render(gs)

    pygame.quit()


main(WIN)
