import math
from common import constants
from .player import Player
from .minotaur import Minotaur
from .maze import Maze
from .cell import Cell
from .direction import *
from collections import deque


def index_string(n: int) -> str:
    special_cases = {1: "first", 2: "second", 3: "third", 8: "eighth"}
    if n in special_cases:
        return special_cases[n]
    else:
        return str(n) + "th"


class GameStateChange:
    def __init__(self, time: int):
        self.time = time
        self.player_positions: dict[str, CoordPair] = {}


class GameState:
    def __init__(self, maze: Maze):
        self.players: list[Player] = []
        self.minotaur = None
        self.maze = maze
        self._all_player_mem: dict[Player, deque[tuple[int, list[Cell]]]] = {}
        self.time: int = 0
        self.escapes = 0

    def add_player(self, player: Player):  # if there is no minotaur, add as minotaur
        if self.minotaur is None:
            if isinstance(player, Minotaur):
                self.minotaur = player
            else:
                mino = Minotaur(player.get_pos(), player.size, constants.MINOTAUR_IMG)
                self.minotaur = mino
        self.players.append(player)
        self._all_player_mem[player] = deque()

    def advance_timeline(self, frames) -> GameStateChange:
        change = GameStateChange(frames)
        self.time += frames
        if self.minotaur:
            self.minotaur.chase_player(self.maze, self.players)
        for player in self.players:
            new_pos = self._move_player(player, frames)
            change.player_positions[player.name] = new_pos
            self._update_player_vision(player)
        self.check_win_lose()
        return change

    def get_player_vision(self, player: Player) -> set[Cell]:
        # minotaur has allvision
        if isinstance(player, Minotaur):
            return set(self.maze.get_cells())

        player_mem = self._all_player_mem[player]
        res: set[Cell] = set()
        for mem_entry in player_mem:
            res.update(mem_entry[1])
        return res

    def _update_player_vision(self, player: Player):
        if isinstance(player, Minotaur):
            return
        player_cell = self.maze.get_cell(player.get_center())
        current_vision = player_cell.get_visible_cells()
        if not self._all_player_mem[player] or self._all_player_mem[player][-1][1] != current_vision:
            self._all_player_mem[player].append((self.time, current_vision))
        else:
            self._all_player_mem[player][-1] = (self.time, self._all_player_mem[player][-1][1])
        while self._all_player_mem and self.time - self._all_player_mem[player][0][0] > constants.PLAYER_MEM_SIZE:
            self._all_player_mem[player].popleft()

    def check_win_lose(self) -> Optional[dict[Player, bool]]:
        res = {}
        for player in self.players:
            if player == self.minotaur:
                continue
            player_cell = self.maze.get_cell(player.get_center())

            dist = player.get_center() - self.minotaur.get_center()
            abs_dist = math.sqrt(abs(dist.x)**2 + abs(dist.y)**2)
            res[player] = abs_dist < constants.KILL_DIST
            if res[player]:
                self.kill_player(player)

            if player_cell == self.maze.victory_cell:
                self.escapes += 1
                return None
        return res

    def kill_player(self, player):
        player.is_alive = False
        self._all_player_mem[player].clear()

    def _move_player(self, player: Player, frames: int) -> CoordPair:
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
        return CoordPair(target_x, target_y)

    def reset(self):
        self.maze = Maze(constants.ROWS, constants.WIDTH)
        self.maze.generate_labyrinth()

        center = (constants.ROWS // 2 + 0.5) * self.maze.cell_width
        player_start = CoordPair(center, center)
        mino_start = self.maze.get_random_edge_cell().get_pos()
        self.minotaur.set_pos(mino_start)

        for player in self.players:
            if player == self.minotaur:
                continue
            player.is_alive = True
            player.set_pos(player_start)

    def apply_change(self, change: GameStateChange):
        self.time += change.time
        for player in self.players:
            new_pos = change.player_positions.get(player.name)
            if new_pos:
                player.center(new_pos.x, new_pos.y)
            self._update_player_vision(player)

    def populate(self, other: 'GameState'):
        self.time = other.time
        if len(self.players) != len(other.players):
            raise Exception("Invalid populate: different player count")

        # copy player attributes
        for i in range(len(self.players)):
            self_player = self.players[i]
            targ_player = other.players[i]
            targ_pos = targ_player.get_center()
            targ_dir = targ_player.move_direction
            self_player.center(targ_pos.x, targ_pos.y)
            self_player.move_direction = CoordPair(targ_dir.x, targ_dir.y)
            self_player.is_alive = targ_player.is_alive



