import constants
import maze
from player import Player
from minotaur import Minotaur
from maze import Maze
from cell import Cell
from direction import *
from collections import deque


def index_string(n: int) -> str:
    special_cases = {1: "first", 2: "second", 3: "third", 8: "eighth"}
    if n in special_cases:
        return special_cases[n]
    else:
        return str(n) + "th"


class GameState:
    def __init__(self, player: Player, minotaur: Minotaur, maze: Maze):
        self.player = player
        self.minotaur = minotaur
        self.maze = maze
        self._player_mem: deque[tuple[int, list[Cell]]] = deque()
        self.time = 0
        self.escapes = 0

    def advance_timeline(self, frames):
        self.time += frames
        self._move_player(self.player, frames)
        self.minotaur.chase_player(self.maze, self.player)
        self._move_player(self.minotaur, frames)
        self._update_player_vision()

    def _update_player_vision(self):
        player_cell = self.maze.get_cell(self.player.get_center())
        current_vision = player_cell.get_visible_cells()
        if not self._player_mem or self._player_mem[-1][1] != current_vision:
            self._player_mem.append((self.time, current_vision))
        else:
            self._player_mem[-1] = (self.time, self._player_mem[-1][1])
        while self._player_mem and self.time - self._player_mem[0][0] > constants.PLAYER_MEM_SIZE:
            self._player_mem.popleft()

        vision = self.get_complete_vision()

        def paint_cell(cell):
            if cell in vision:
                cell.change_color(constants.WHITE)
            else:
                cell.change_color(constants.BLACK)

        self.maze.process_cells(paint_cell)

    def get_complete_vision(self) -> set[Cell]:
        res = set()
        for vision in self._player_mem:
            for cell in vision[1]:
                res.add(cell)
        return res

    def check_win_lose(self) -> Optional[bool]:
        player_cell = self.maze.get_cell(self.player.get_center())
        minotaur_cell = self.maze.get_cell(self.minotaur.get_center())

        if player_cell == minotaur_cell:
            return False
        if player_cell == self.maze.victory_cell:
            self.escapes += 1
            return True

        return None

    def _move_player(self, player: Player, frames: int):
        x, y = player.get_center()
        dx, dy = player.move_direction
        target_x = min(self.maze.width - 1, x + dx * player.speed * frames)
        target_y = min(self.maze.width - 1, y + dy * player.speed * frames)

        current_cell = self.maze.get_cell(CoordPair(x, y))
        target_x_cell = self.maze.get_cell(CoordPair(target_x, y))
        target_y_cell = self.maze.get_cell(CoordPair(x, target_y))

        curr_x, curr_y = current_cell.get_pos()
        if current_cell != target_x_cell:
            if not current_cell.is_neighbor(target_x_cell):
                if dx > 0:  # moving right
                    target_x = curr_x + current_cell.width - 1
                else:  # moving left
                    target_x = curr_x
            else:
                target_x_cell.request_update()

        if current_cell != target_y_cell:
            if not current_cell.is_neighbor(target_y_cell):
                if dy > 0:  # moving down
                    target_y = curr_y + current_cell.width - 1
                else:  # moving up
                    target_y = curr_y
            else:
                target_y_cell.request_update()

        player.center(target_x, target_y)
