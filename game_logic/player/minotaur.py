import random
from .player import Player
from game_logic.direction import *
from game_logic.maze.pathfinding import PathfindingRes, astar
from game_logic.maze import Maze
from game_logic.player.modifier.le_modifier import ModifierType
from game_logic.player.modifier import mino_acceleration_modifier as mam
from common import constants


class Minotaur(Player):
    def __init__(self, pos: CoordPair, radius: float, is_player_controlled=False, name="Minotaur"):
        super().__init__(pos, radius, name=name, alive_img=constants.MINOTAUR_IMG)
        self.speed = constants.MINOTAUR_SPEED
        self.chased_player = None
        self.is_player_controlled = is_player_controlled
        self.prev_move_dir = CoordPair(self.move_direction.x, self.move_direction.y)

    def chase_player(self, maze: Maze, players: list[Player]) -> None:
        if self.is_player_controlled:
            return
        players_without_self = [p for p in players if p != self]
        if self.chased_player is None:
            self.chased_player = random.choice(players_without_self)
        curr_cell = maze.get_cell(self.center)
        player_cell = maze.get_cell(self.chased_player.center)
        path: PathfindingRes = astar(curr_cell, player_cell)
        if len(path.path) == 1:
            target = self.chased_player.center
        else:
            target = path[1].get_center()
        self.move_direction = target - self.center

    def move(self, vector: CoordPair = None, ticks: int = None):
        vector = super().move(vector, ticks)
        # acceleration
        accel_mod = mam.MinoAccelerationModifier(self.move_direction)
        self._modifiers[ModifierType.Speed].append(accel_mod)

    def update_modifiers(self, ticks: int):
        # remove acceleration after direction change
        for spd_mod in self._modifiers[ModifierType.Speed]:
            if not isinstance(spd_mod, mam.MinoAccelerationModifier):
                continue
            if spd_mod.move_dir.angle_between(self.move_direction.normalize()) > mam.MAX_ANGLE:
                spd_mod.is_active = False
        super().update_modifiers(ticks)
