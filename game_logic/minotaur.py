import random
from .player import Player
from .direction import *
from .pathfinding import PathfindingRes, astar
from .maze import Maze
from common.constants import *


class Minotaur(Player):
    def __init__(self, pos: CoordPair, size: tuple[int, int], is_player_controlled=False, name="Minotaur"):
        super().__init__(pos, size, name=name, alive_img=MINOTAUR_IMG)
        self.speed = MINOTAUR_SPEED
        self.chased_player = None
        self.is_player_controlled = is_player_controlled

    def chase_player(self, maze: Maze, players: list[Player]) -> None:
        if self.is_player_controlled:
            return
        players_without_self = [p for p in players if p != self]
        if self.chased_player is None:
            self.chased_player = random.choice(players_without_self)
        curr_cell = maze.get_cell(self.get_center())
        player_cell = maze.get_cell(self.chased_player.get_center())
        path: PathfindingRes = astar(curr_cell, player_cell)
        if path.path.__len__() == 1:
            self.move_direction = get_move_direction(self.get_center(), self.chased_player.get_center())
        else:
            self.move_direction = get_move_direction(self.get_center(), path[1].get_center())
