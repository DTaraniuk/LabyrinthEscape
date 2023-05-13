from player import Player
from maze import Maze
from pathfinding import astar, PathfindingRes
from direction import *
from constants import *
import pygame


class Minotaur(Player):
    def __init__(self, pos: CoordPair, size: tuple[int, int], img: pygame.Surface = None):
        super().__init__(pos, size, img)
        self.speed = MINOTAUR_SPEED

    def chase_player(self, maze: Maze, player: Player) -> bool:
        # victory check
        curr_pos = self.get_center()
        curr_cell = maze.get_cell(curr_pos)
        player_cell = maze.get_cell(player.get_center())
        if player_cell == curr_cell:
            return True

        path: PathfindingRes = astar(curr_cell, player_cell)
        if not path[0] == curr_cell:
            raise RuntimeError(f"{path[0]} does not equal {curr_cell}. Astar fail")
        next_cell = path[1]
        move_direction = get_move_direction(self.get_center(), next_cell.get_center())
        self.move(move_direction, maze)

        return False
