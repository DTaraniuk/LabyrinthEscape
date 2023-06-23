import math
from common import constants
from .player import Player, PlayerState
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
    def __init__(self, step: int):
        self.step = step
        self.player_positions: dict[str, CoordPair] = {}
        self.player_directions: dict[str, CoordPair] = {}
        self.player_states: dict[str, PlayerState] = {}


class GameState:
    def __init__(self, maze: Maze):
        self.players: dict[str, Player] = {}
        self.minotaur = None
        self.maze = maze
        self._all_player_mem: dict[str, deque[tuple[int, list[Cell]]]] = {}
        self.step: int = 0

    def add_player(self, player: Player):  # if there is no minotaur, add as minotaur
        if self.minotaur is None:
            if isinstance(player, Minotaur):
                self.minotaur = player
            else:
                mino = Minotaur(player.get_pos(), player.size, constants.MINOTAUR_IMG)
                self.minotaur = mino
        self.players[player.name] = player
        self._all_player_mem[player.name] = deque()

    def advance_timeline(self, frames) -> GameStateChange:
        self.step += frames
        change = GameStateChange(self.step)
        if self.minotaur:
            self.minotaur.chase_player(self.maze, list(self.players.values()))
        for player in self.players.values():
            if player.state == PlayerState.DEAD:
                continue

            self._move_player(player, frames)
            change.player_positions[player.name] = player.get_pos()
            change.player_directions[player.name] = player.move_direction
            self._update_player_vision(player)
        state_update = self.check_win_lose()
        for name, state in state_update.items():
            change.player_states[name] = state

        return change

    def get_player_vision(self, player: Player) -> set[Cell]:
        # minotaur has allvision
        if isinstance(player, Minotaur):
            return set(self.maze.get_cells())

        player_mem = self._all_player_mem[player.name]
        res: set[Cell] = set()
        for mem_entry in player_mem:
            res.update(mem_entry[1])
        return res

    def _update_player_vision(self, player: Player):
        if isinstance(player, Minotaur):
            return
        player_cell = self.maze.get_cell(player.get_center())
        current_vision = player_cell.get_visible_cells()
        if not self._all_player_mem[player.name] or self._all_player_mem[player.name][-1][1] != current_vision:
            self._all_player_mem[player.name].append((self.step, current_vision))
        else:
            self._all_player_mem[player.name][-1] = (self.step, self._all_player_mem[player.name][-1][1])
        while self._all_player_mem and self.step - self._all_player_mem[player.name][0][0] > constants.PLAYER_MEM_SIZE:
            self._all_player_mem[player.name].popleft()

    def check_win_lose(self) -> dict[str, PlayerState]:
        res = {}
        for player in self.players.values():
            if player == self.minotaur or player.state != PlayerState.ALIVE:
                continue
            player_cell = self.maze.get_cell(player.get_center())

            dist = player.get_center() - self.minotaur.get_center()
            abs_dist = math.sqrt(abs(dist.x)**2 + abs(dist.y)**2)
            player_dead = abs_dist < constants.KILL_DIST
            if player_dead:
                self.kill_player(player)
                res[player.name] = PlayerState.DEAD

            if player_cell == self.maze.victory_cell:
                player.state = PlayerState.ESCAPED
                res[player.name] = PlayerState.ESCAPED
        return res

    def kill_player(self, player):
        player.state = PlayerState.DEAD
        self._all_player_mem[player.name].clear()

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

        if current_cell != target_y_cell:
            if not current_cell.is_neighbor(target_y_cell):
                if dy > 0:  # moving down
                    target_y = curr_y + current_cell.width - 1
                else:  # moving up
                    target_y = curr_y

        player.center(target_x, target_y)

    def reset(self):
        self.maze = Maze(constants.ROWS, constants.WIDTH)
        self.maze.generate_labyrinth()

        center = (constants.ROWS // 2 + 0.5) * self.maze.cell_width
        player_start = CoordPair(center, center)
        mino_start = self.maze.get_random_edge_cell().get_pos()
        self.minotaur.set_pos(mino_start)

        for player in self.players.values():
            if player == self.minotaur:
                continue
            player.state = PlayerState.ALIVE
            player.set_pos(player_start)

    def apply_change(self, change: GameStateChange):
        self.step = change.step
        for name, player in self.players.items():
            # Ensure the player's name exists in the dictionary before attempting to access it
            if name in change.player_states:
                player.state = change.player_states[player.name]
            if name in change.player_positions:
                player.set_pos(change.player_positions[player.name])
            if name in change.player_directions:
                player.move_direction = change.player_directions[player.name]

            self._update_player_vision(player)

    def update_player_direction(self, name: str, new_direction: CoordPair, time: int):
        player = self.players.get(name)
        if not player:
            return
        if time < self.step:    # we need to adjust the position due to outdated direction update
            adjustment = (new_direction - player.move_direction) * (self.step - time) * player.speed
            player.set_pos(player.get_pos() + adjustment)
        player.move_direction = new_direction

