import random

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
        self.chased_player = None

    def chase_player(self, maze: Maze, players: list[Player]) -> None:
        if self.chased_player is None:
            self.chased_player = random.choice(players)
        curr_cell = maze.get_cell(self.get_center())
        player_cell = maze.get_cell(self.chased_player.get_center())
        path: PathfindingRes = astar(curr_cell, player_cell)
        if path.path.__len__() == 1:
            self.move_direction = get_move_direction(self.get_center(), self.chased_player.get_center())
        else:
            self.move_direction = get_move_direction(self.get_center(), path[1].get_center())
