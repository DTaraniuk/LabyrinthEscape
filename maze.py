import random
from cell import Cell
from typing import Callable, Optional


class Maze:
    def __init__(self, rows: int = None, width: int = None):
        self.maze: list[list[Cell]] = []
        self.visited_cells: list[list[bool]] = []
        self.rows = 0
        self.width = 0
        self.cell_width = 0.0
        if rows and width:
            self.rows = rows
            self.width = width
            self.cell_width = width // rows
            for i in range(rows):
                self.maze.append([])
                self.visited_cells.append([])
                for j in range(rows):
                    cell = Cell(i, j, self.cell_width, rows)
                    self.maze[i].append(cell)
                    self.visited_cells[i].append(False)

    def carve_path(self, x: int, y: int) -> None:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        cell: Cell = self.maze[x][y]
        self.visited_cells[x][y] = True

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.rows and not self.visited_cells[nx][ny]:
                neighbor: Cell = self.maze[nx][ny]
                neighbor.neighbors.append(cell)
                cell.neighbors.append(neighbor)
                self.carve_path(nx, ny)

    def generate_labyrinth(self) -> None:
        start_x, start_y = random.randrange(0, self.rows), random.randrange(0, self.rows)
        self.carve_path(start_x, start_y)

    def get_cells(self) -> list[Cell]:
        res = []
        for row in self.maze:
            for cell in row:
                res.append(cell)
        return res

    def process_cells(self, operation: Callable[[Cell], object]):
        for cell in self.get_cells():
            operation(cell)

    def request_full_update(self):
        self.process_cells(lambda c: setattr(c, 'is_up_to_date', False))

    def get_cell(self, x, y) -> Optional[Cell]:
        if x >= self.rows or y >= self.rows:
            return None
        return self.maze[x][y]

