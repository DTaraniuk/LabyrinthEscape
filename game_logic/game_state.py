import math

from common import constants
from .player import LePlayer, PlayerState
from .player.le_minotaur import LeMinotaur
from .player.modifier.le_modifier import LeModifier
from .maze import Maze
from game_logic.maze.cell import Cell
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
        self.player_modifiers: dict[str, list[LeModifier]] = {}


class GameState:
    def __init__(self, maze: Maze, write_changes: bool = False):
        self.players: dict[str, LePlayer] = {}
        self.minotaur: LeMinotaur = None
        self.maze = maze
        self._all_player_mem: dict[str, deque[tuple[int, list[Cell]]]] = {}
        self.step: int = 0
        self.write_changes: bool = write_changes
        self.changes: list[GameStateChange] = []

    def add_player(self, player: LePlayer):  # if there is no minotaur, add as minotaur
        if self.minotaur is None:
            if isinstance(player, LeMinotaur):
                self.minotaur = player
            else:
                mino = LeMinotaur(player.pos, player.size, constants.MINOTAUR_IMG)
                self.minotaur = mino
        self.players[player.name] = player
        self._all_player_mem[player.name] = deque()

    def advance_timeline(self, ticks):
        self.step += ticks
        change = GameStateChange(self.step)
        if self.minotaur:
            self.minotaur.chase_player(self.maze, list(self.players.values()))
        for player in self.players.values():
            if player.state == PlayerState.DEAD:
                continue

            old_modifiers = player.get_modifiers()
            self._move_player(player, ticks)
            change.player_positions[player.name] = player.pos
            change.player_directions[player.name] = player.move_direction
            self._update_player_vision(player)
            new_modifiers = player.get_modifiers()
            change.player_modifiers[player.name] = list([m for m in new_modifiers if m not in old_modifiers])
        state_update = self.check_win_lose()
        for name, state in state_update.items():
            change.player_states[name] = state

        if self.write_changes:
            self.changes.append(change)

    def get_player_vision(self, player: LePlayer) -> set[Cell]:
        # minotaur has allvision
        if isinstance(player, LeMinotaur):
            return set(self.maze.get_cells())

        player_mem = self._all_player_mem[player.name]
        res: set[Cell] = set()
        for mem_entry in player_mem:
            res.update(mem_entry[1])
        return res

    def _update_player_vision(self, player: LePlayer):
        if isinstance(player, LeMinotaur):
            return
        player_cell = self.maze.get_cell(player.center)
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
            player_cell = self.maze.get_cell(player.center)
            mino_cell = self.maze.get_cell(self.minotaur.center)

            dist = player.center - self.minotaur.center
            abs_dist = math.sqrt(abs(dist.x)**2 + abs(dist.y)**2)
            catch_cells = list(player_cell.get_neighbors().values())
            catch_cells.append(player_cell)
            is_player_dead = abs_dist < constants.KILL_DIST and mino_cell in catch_cells
            if is_player_dead:
                self.kill_player(player)
                res[player.name] = PlayerState.DEAD

            if player_cell == self.maze.victory_cell:
                player.state = PlayerState.ESCAPED
                res[player.name] = PlayerState.ESCAPED
        return res

    def kill_player(self, player):
        player.state = PlayerState.DEAD
        self._all_player_mem[player.name].clear()

    def _move_player(self, player: LePlayer, ticks: int):
        player.update_modifiers(ticks)
        move_vector = player.move(ticks)
        target_x = max(1, min(self.maze.width - 1, move_vector.x))
        target_y = max(1, min(self.maze.width - 1, move_vector.y))

        x, y = player.center.to_tuple()
        current_cell = self.maze.get_cell(CoordPair(x, y))
        target_x_cell = self.maze.get_cell(CoordPair(target_x, y))
        target_y_cell = self.maze.get_cell(CoordPair(x, target_y))

        curr_x, curr_y = current_cell.get_pos()
        if current_cell != target_x_cell:
            if not current_cell.is_neighbor(target_x_cell):
                if player.move_direction.x > 0:  # moving right
                    target_x = curr_x + current_cell.width - 1
                else:  # moving left
                    target_x = curr_x

        if current_cell != target_y_cell:
            if not current_cell.is_neighbor(target_y_cell):
                if player.move_direction.y > 0:  # moving down
                    target_y = curr_y + current_cell.width - 1
                else:  # moving up
                    target_y = curr_y

        player.center = (target_x, target_y)

    def reset(self):
        self.maze = Maze(constants.ROWS, constants.WIDTH)
        self.maze.generate_labyrinth()

        center = (constants.ROWS // 2 + 0.5) * self.maze.cell_width
        player_start = CoordPair(center, center)
        mino_start = self.maze.get_random_edge_cell().get_pos()
        self.minotaur.pos = mino_start

        for player in self.players.values():
            if player == self.minotaur:
                continue
            player.state = PlayerState.ALIVE
            player.pos = player_start

    def get_aggregated_changes(self) -> GameStateChange:
        if not self.write_changes:
            raise Exception("Attempted to get changes when they are not recorded.")
        bulk_change = GameStateChange(self.step)
        for single_change in self.changes:
            bulk_change.player_positions.update(single_change.player_positions)
            bulk_change.player_directions.update(single_change.player_directions)
            bulk_change.player_states.update(single_change.player_states)
            for player, modifiers in single_change.player_modifiers.items():
                if player not in bulk_change.player_modifiers:
                    bulk_change.player_modifiers[player] = modifiers.copy()
                else:
                    bulk_change.player_modifiers[player].extend(modifiers)
        self.changes.clear()
        return bulk_change

    def apply_change(self, change: GameStateChange):
        self.step = change.step
        for name, player in self.players.items():
            # Ensure the player's name exists in the dictionary before attempting to access it
            if name in change.player_states:
                player.state = change.player_states[player.name]
            if name in change.player_positions:
                player.pos = change.player_positions[player.name]
            if name in change.player_directions:
                player.move_direction = change.player_directions[player.name]
            if name in change.player_modifiers:
                player.add_modifiers(change.player_modifiers[name])

            self._update_player_vision(player)

    def update_player_direction(self, name: str, new_direction: CoordPair, time: int):
        player = self.players.get(name)
        if not player:
            return
        if time < self.step:    # we need to adjust the position due to outdated direction update
            adjustment = (new_direction - player.move_direction) * (self.step - time) * player.speed
            player.pos += adjustment
        player.move_direction = new_direction

