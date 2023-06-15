import random
from .cell import Cell
from typing import Callable, Optional
from common import constants
from .direction import Direction
from .coordpair import CoordPair


def request_update(cells: list[Cell]):
    for c in cells:
        c.request_update()


class Maze:
    def __init__(self, rows: int = None, width: int = None):
        self.maze: list[list[Cell]] = []
        self.row_num = 0
        self.width = 0
        self.cell_width = 0.0
        self._victory_cell: Cell = None
        if rows and width:
            self.row_num = rows
            self.width = width
            self.cell_width = width // rows
            for i in range(rows):
                self.maze.append([])
                for j in range(rows):
                    cell = Cell(i, j, self.cell_width, rows)
                    self.maze[i].append(cell)
        self.randomize_victory_cell()

    @property
    def victory_cell(self):
        return self._victory_cell

    @victory_cell.setter
    def victory_cell(self, value):
        self._victory_cell = value

    def carve_path(self, x: int, y: int, cell_visit_data: list[list[int]], max_visits: int) -> None:
        directions = list(Direction)
        random.shuffle(directions)

        cell: Cell = self.maze[x][y]
        cell_visit_data[x][y] += 1

        for direction in directions:
            dx, dy = direction.value
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.row_num and 0 <= ny < self.row_num and cell_visit_data[nx][ny] < max_visits:
                neighbor: Cell = self.maze[nx][ny]
                cell.add_neighbor(neighbor, direction)
                self.carve_path(nx, ny, cell_visit_data, max_visits)

    def remove_random_walls(self, wall_count: int) -> int:
        shuffled_cells: list[Cell] = self.get_cells()
        random.shuffle(shuffled_cells)
        directions = list(Direction)
        cnt = 0
        for cell in shuffled_cells:
            if cnt == wall_count:
                return cnt
            random.shuffle(directions)
            for direction in directions:
                dx, dy = direction.value
                x, y = cell.get_index()
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.row_num and 0 <= ny < self.row_num:
                    candidate_cell = self[nx, ny]
                    if not cell.is_neighbor(candidate_cell):
                        cell.add_neighbor(candidate_cell)
                        cnt += 1
                        break

    def generate_labyrinth(self) -> None:
        cell_visit_data: list[list[int]] = []
        for row_i in range(self.row_num):
            cell_visit_data.append([])
            for col_i in range(self.row_num):
                cell_visit_data[row_i].append(0)
        start_x, start_y = random.randrange(0, self.row_num), random.randrange(0, self.row_num)
        self.carve_path(start_x, start_y, cell_visit_data, 1)

        self.remove_random_walls(constants.RAND_WALL_COUNT)

    def get_cells(self) -> list[Cell]:
        res = []
        for row in self.maze:
            for cell in row:
                res.append(cell)
        return res

    def process_cells(self, operation: Callable[[Cell], None]):
        for cell in self.get_cells():
            operation(cell)

    def request_full_update(self):
        self.process_cells(lambda c: setattr(c, 'is_up_to_date', False))

    def __getitem__(self, index: tuple[int, int]) -> Optional[Cell]:
        x, y = index
        return self.maze[x][y]

    def get_cell(self, coords: CoordPair) -> Optional[Cell]:
        index: tuple[int, int] = int(coords.x // self.cell_width), int(coords.y // self.cell_width)
        return self[index]

    def get_random_edge_cell(self):
        edge_length = self.row_num
        edge_choice = random.choice(["top", "bottom", "left", "right"])

        if edge_choice == "top":
            res = self[0, random.randint(0, edge_length - 1)]
        elif edge_choice == "bottom":
            res = self[edge_length - 1, random.randint(0, edge_length - 1)]
        elif edge_choice == "left":
            res = self[random.randint(0, edge_length - 1), 0]
        else:  # edge_choice == "right"
            res = self[random.randint(0, edge_length - 1), edge_length - 1]

        return res

    def randomize_victory_cell(self):
        # if self._victory_cell:
        #     self._victory_cell.color = WHITE

        self.victory_cell = self.get_random_edge_cell()
        # self.victory_cell.color = PINK
