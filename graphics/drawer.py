import pygame
from game_logic import Cell, Player, Direction, Wall
from common import constants


def draw_cell(cell: Cell, pgs: pygame.Surface) -> None:
    if cell.is_updated:
        return
    width: int = cell.width
    x, y = cell.index_in_row * width, cell.index_in_col * width
    pygame.draw.rect(pgs, cell.color, (x, y, width, width))

    cell.is_updated = True


def draw_player(player: Player, image: pygame.Surface, pgs: pygame.Surface):
    center = player.center
    circle = player.get_area()
    topleft = (center.x - circle.radius, center.y - circle.radius)

    # draw player circle
    pygame.draw.circle(surface=pgs,
                       color=constants.PLAYER_CIRCLE_COLOR,
                       width=constants.PLAYER_CIRCLE_WIDTH,
                       radius=circle.radius,
                       center=center.to_tuple())

    # Blit the player image
    pgs.blit(image, topleft)

    # Render the text. "True" means anti-aliased text.
    text = constants.PLAYER_NAME_FONT.render(player.name, True, constants.ORANGE)

    # Blit the text surface onto the pgs surface.
    text_pos = topleft[0], topleft[1] + image.get_height()
    pgs.blit(text, text_pos)


def draw_grid(grid_surface: pygame.Surface, color: tuple[int, int, int]):
    cell_width = constants.WIDTH / constants.ROWS
    for i in range(constants.ROWS):
        pygame.draw.line(grid_surface, color, (0, i * cell_width), (constants.WIDTH, i * cell_width))
        pygame.draw.line(grid_surface, color, (i * cell_width, 0), (i * cell_width, constants.WIDTH))


def draw_wall(wall_surface: pygame.Surface, wall: Wall):
    if wall.is_updated:
        return

    wall_surface.fill(wall.color, wall.area)
    wall.requires_update = False

    wall.is_updated = True

