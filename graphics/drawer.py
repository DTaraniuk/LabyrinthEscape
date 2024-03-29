import pygame
from game_logic import Cell, LePlayer, Direction
from common import constants


def draw_cell(cell: Cell, pgs: pygame.Surface) -> None:
    if cell.is_updated:
        return
    width: int = cell.width
    x, y = cell.index_in_row * width, cell.index_in_col * width
    pygame.draw.rect(pgs, cell.color, (x, y, width, width))

    sides = list(Direction)
    for direction in cell.get_neighbors().keys():
        if direction in sides:
            sides.remove(direction)

    for direction in sides:
        wx1: int = x
        wx2: int = x
        wy1: int = y
        wy2: int = y
        if direction == Direction.SOUTH:  # DOWN
            wx2 += width - constants.WALL_WIDTH
            wy1 += width - constants.WALL_WIDTH
            wy2 += width - constants.WALL_WIDTH
        if direction == Direction.NORTH:  # UP
            wx2 += width
        if direction == Direction.EAST:  # RIGHT
            wx1 += width - constants.WALL_WIDTH
            wx2 += width - constants.WALL_WIDTH
            wy2 += width - constants.WALL_WIDTH
        if direction == Direction.WEST:  # LEFT
            wy2 += width
        pygame.draw.line(pgs, constants.RED, (wx1, wy1), (wx2, wy2), constants.WALL_WIDTH)

    cell.is_updated = True


def draw_player(player: LePlayer, image: pygame.Surface, pgs: pygame.Surface):
    # Blit the player image
    pgs.blit(image, player.pos.to_tuple())

    # Render the text. "True" means anti-aliased text.
    # (The last parameter is color.)
    text = constants.PLAYER_NAME_FONT.render(player.name, True, constants.ORANGE)

    # Blit the text surface onto the pgs surface.
    # We need to decide where to blit - Let's put it just below the player image.
    text_pos = player.pos.x, player.pos.y + image.get_height()
    pgs.blit(text, text_pos)


def draw_grid(grid_surface: pygame.Surface, color: tuple[int, int, int]):
    cell_width = constants.WIDTH / constants.ROWS
    for i in range(constants.ROWS):
        pygame.draw.line(grid_surface, color, (0, i * cell_width), (constants.WIDTH, i * cell_width))
        pygame.draw.line(grid_surface, color, (i * cell_width, 0), (i * cell_width, constants.WIDTH))
