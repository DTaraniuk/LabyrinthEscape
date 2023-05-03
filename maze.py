import random
from typing import List, Tuple, Callable
from cell import Cell


def make_maze(rows: int, width: int) -> List[List[Cell]]:
    grid = []
    cell_width = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, cell_width, rows)
            grid[i].append(cell)
            
    return grid


def carve_path(x: int, y: int, grid: List[List[Cell]], total_rows: int) -> None:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)

    cell: Cell = grid[x][y]
    cell.visited = True

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < total_rows and 0 <= ny < total_rows and not grid[nx][ny].visited:
            neighbor: Cell = grid[nx][ny]
            neighbor.neighbors.append(cell)
            cell.neighbors.append(neighbor)
            carve_path(nx, ny, grid, total_rows)


def generate_labyrinth(maze: List[List[Cell]], total_rows: int) -> None:
    start_x, start_y = random.randrange(0, total_rows), random.randrange(0, total_rows)
    carve_path(start_x, start_y, maze, total_rows)

