import random

import pygame

from .cell import Cell
from .wall import Wall, WallType
from typing import Callable, Optional
from common import constants
from game_logic.direction import Direction
from game_logic.coordpair import CoordPair


class Maze:
    def __init__(self, rows: int = 0, width: int = 0):
        self.cells: list[list[Cell]] = []
        self.walls: list[list[Wall]] = []
        self.row_num = rows
        self.width = width
        self.cell_width = width // rows

        # init walls
        self.__init_walls_and_cells()

        self._victory_cell: Cell = None
        self.randomize_victory_cell()

    @property
    def victory_cell(self):
        return self._victory_cell

    @victory_cell.setter
    def victory_cell(self, value):
        self._victory_cell = value

    def __init_walls_and_cells(self):
        wall_width = constants.WALL_WIDTH
        cell_width = self.cell_width
        rows = self.row_num

        # Initialize horizontal and vertical walls separately
        hor_walls = []
        ver_walls = []

        for i in range(rows + 1):  # Create horizontal walls
            hor_walls.append([])
            for j in range(rows):
                y = i * cell_width - wall_width
                height = wall_width * 2
                if y < 0:  # Topmost wall, outside the maze
                    y = 0
                    height = wall_width
                wall_rect = pygame.Rect(j * cell_width, y, cell_width, height)
                hor_walls[i].append(Wall(wall_rect))

        for i in range(rows):  # Create vertical walls
            ver_walls.append([])
            for j in range(rows + 1):
                x = j * cell_width - wall_width
                width = wall_width * 2
                if x < 0:  # Leftmost wall, outside the maze
                    width = wall_width
                    x = 0
                wall_rect = pygame.Rect(x, i * cell_width, width, cell_width)
                ver_walls[i].append(Wall(wall_rect))

        # Init cells and associate walls with them
        for i in range(rows):
            self.cells.append([])
            for j in range(rows):
                cell = Cell(i, j, self.cell_width)
                self.cells[i].append(cell)

                # Associate walls with the cell
                error_msg = f'Indexing error during wall creation: i={i}, j={j}'
                # Horizontal walls
                if i < len(hor_walls):  # Wall above
                    cell.add_wall(hor_walls[i][j], Direction.NORTH)
                else:
                    print(error_msg)
                if (i + 1) < len(hor_walls):  # Wall below
                    cell.add_wall(hor_walls[i + 1][j], Direction.SOUTH)
                else:
                    print(error_msg)

                # Vertical walls
                if j < len(ver_walls[i]):  # Wall on the left
                    cell.add_wall(ver_walls[i][j], Direction.WEST)
                else:
                    print(error_msg)
                if (j + 1) < len(ver_walls[i]):  # Wall on the right
                    cell.add_wall(ver_walls[i][j + 1], Direction.EAST)
                else:
                    print(error_msg)

    def carve_path(self, x: int, y: int, cell_visit_data: list[list[int]], max_visits: int) -> None:
        directions = list(Direction)
        random.shuffle(directions)

        cell: Cell = self.cells[x][y]
        cell_visit_data[x][y] += 1

        for direction in directions:
            dx, dy = direction.value
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.row_num and 0 <= ny < self.row_num and cell_visit_data[nx][ny] < max_visits:
                neighbor: Cell = self.cells[nx][ny]
                cell.add_neighbor(neighbor, direction)
                self.carve_path(nx, ny, cell_visit_data, max_visits)

    def remove_random_walls(self, wall_count: int) -> None:
        directions = list(Direction)
        cnt = 0
        while cnt < wall_count:
            cell = random.choice(self.get_cells())
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
        for row in self.cells:
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
        return self.cells[x][y]

    def get_cell(self, coords: CoordPair) -> Optional[Cell]:
        index: tuple[int, int] = int(coords.x // self.cell_width), int(coords.y // self.cell_width)
        return self[index]

    def get_random_edge_cell(self) -> Cell:
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
        self.victory_cell.color = constants.PINK
