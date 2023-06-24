import random
from .le_player import LePlayer
from game_logic.direction import *
from game_logic.pathfinding import PathfindingRes, astar
from game_logic.maze import Maze
from game_logic.player.modifier.le_modifier import LeModifierType
from game_logic.player.modifier.le__acceleration_modifier import LeAccelerationModifier
from common.constants import *


class LeMinotaur(LePlayer):
    def __init__(self, pos: CoordPair, size: tuple[int, int], is_player_controlled=False, name="Minotaur"):
        super().__init__(pos, size, name=name, alive_img=MINOTAUR_IMG)
        self.speed = MINOTAUR_SPEED
        self.chased_player = None
        self.is_player_controlled = is_player_controlled
        self.prev_move_dir = CoordPair(self.move_direction.x, self.move_direction.y)

    def chase_player(self, maze: Maze, players: list[LePlayer]) -> None:
        if self.is_player_controlled:
            return
        players_without_self = [p for p in players if p != self]
        if self.chased_player is None:
            self.chased_player = random.choice(players_without_self)
        curr_cell = maze.get_cell(self.center)
        player_cell = maze.get_cell(self.chased_player.center)
        path: PathfindingRes = astar(curr_cell, player_cell)
        if path.path.__len__() == 1:
            self.move_direction = get_move_direction(self.center, self.chased_player.center)
        else:
            self.move_direction = get_move_direction(self.center, path[1].get_center())

    def move(self, ticks: int) -> CoordPair:
        vec = super(LeMinotaur, self).move(ticks)
        # acceleration
        accel_mod = LeAccelerationModifier(self.speed*1e-3, LeModifierType.Speed, self.move_direction.clone())
        self._modifiers[LeModifierType.Speed].append(accel_mod)
        return vec
