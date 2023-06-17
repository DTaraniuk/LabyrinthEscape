import pygame
from game_logic import Cell
from common import constants


def draw_cell(cell: Cell, win: pygame.Surface) -> None:
    if cell.is_up_to_date:
        return
    width: int = cell.width
    x, y = cell.index_in_row * width, cell.index_in_col * width
    pygame.draw.rect(win, cell.color, (x, y, width, width))

    sides = {'NORTH', 'SOUTH', 'EAST', 'WEST'}
    for direction in cell.get_neighbors().keys():
        if direction in sides:
            sides.remove(direction)

    for direction in sides:
        wx1: int = x
        wx2: int = x
        wy1: int = y
        wy2: int = y
        if direction == 'SOUTH':  # DOWN
            wx2 += width - constants.WALL_WIDTH
            wy1 += width - constants.WALL_WIDTH
            wy2 += width - constants.WALL_WIDTH
        if direction == 'NORTH':  # UP
            wx2 += width
        if direction == 'EAST':  # RIGHT
            wx1 += width - constants.WALL_WIDTH
            wx2 += width - constants.WALL_WIDTH
            wy2 += width - constants.WALL_WIDTH
        if direction == 'WEST':  # LEFT
            wy2 += width
        pygame.draw.line(win, constants.RED, (wx1, wy1), (wx2, wy2), constants.WALL_WIDTH)
