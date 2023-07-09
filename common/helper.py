from typing import Callable
import pygame
import math
from .constants import *
from game_logic import CoordPair


def wait_for_input():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return


# def read_endpoints() -> tuple[Cell, Cell]:
#     click_num = 0
#     width = WIDTH/ROWS
#     start: Cell = None
#     end: Cell = None
#     while click_num < 2:
#         click = pygame.event.wait()
#         if click.type != pygame.MOUSEBUTTONDOWN:
#             continue
#         x, y = tuple(int(value // width) for value in click.pos)
#         if click_num == 0:
#             start = maze[x, y]
#         else:
#             end = maze[x, y]
#         click_num += 1
#     return start, end


# def handle_pathfinding_call(renderer, maze, algo: Callable[[Cell, Cell], PathfindingRes],
#                             path_color: tuple[int, int, int]):
#     start, end = read_endpoints(maze)
#     pathfinding_res = algo(start, end)
#     for cell in pathfinding_res.affected_nodes:
#         cell.color = cell_color
#         cell.request_update()
#     renderer.render_path(pathfinding_res.path, path_color)
def collide_rect_circle(rect, circle_center, circle_radius):
    circle_distance_x = abs(circle_center[0] - rect.centerx)
    circle_distance_y = abs(circle_center[1] - rect.centery)

    if (circle_distance_x > (rect.w/2 + circle_radius)):
        return False
    if (circle_distance_y > (rect.h/2 + circle_radius)):
        return False

    if (circle_distance_x <= (rect.w/2)):
        return True
    if (circle_distance_y <= (rect.h/2)):
        return True

    corner_distance_sq = (circle_distance_x - rect.w/2)**2 + (circle_distance_y - rect.h/2)**2

    return (corner_distance_sq <= (circle_radius**2))


def input_movement() -> CoordPair:
    keys = pygame.key.get_pressed()
    player_move_vector = CoordPair()
    if keys[pygame.K_UP]:
        player_move_vector += CoordPair(0, -1)
    if keys[pygame.K_DOWN]:
        player_move_vector += CoordPair(0, 1)
    if keys[pygame.K_LEFT]:
        player_move_vector += CoordPair(-1, 0)
    if keys[pygame.K_RIGHT]:
        player_move_vector += CoordPair(1, 0)
    return player_move_vector


def obj_dict(obj):
    """ Recursively convert an object's attributes to a dictionary. """
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("__"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(obj_dict(item))
        else:
            element = obj_dict(val)
        result[key] = element
    return result


def output_obj_to_file(obj, filename):
    """ Output the object to a file. """
    with open(filename, 'w') as file:
        file.write(str(obj_dict(obj)))


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        line_width, _ = font.size(' '.join(current_line))

        if line_width > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def create_text_frame(text: str,
                      font: pygame.font.Font,
                      text_color: tuple[int, int, int],
                      frame_color: tuple[int, int, int],
                      padding: int,
                      aspect_ratio: tuple[int, int]
                      ) -> pygame.Surface:
    # create a surface to get total len
    line_surface = font.render(text, True, text_color)
    length = line_surface.get_width()
    height = font.get_height()
    desired_width = int(math.sqrt(height * aspect_ratio[0] / aspect_ratio[1] * length))

    # Calculate lines with the desired width.
    lines = wrap_text(text, font, desired_width)
    line_surfaces = [font.render(line, True, text_color) for line in lines]
    max_line_width = max(line_surface.get_width() for line_surface in line_surfaces)

    frame_width = max_line_width + 2 * padding
    frame_height = height * lines.__len__() + 2 * padding

    frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
    frame_surface.fill(WHITE)

    pygame.draw.rect(frame_surface, frame_color, (0, 0, frame_width, frame_height), padding)

    for i, line_surface in enumerate(line_surfaces):
        x = padding
        y = padding + i * height
        frame_surface.blit(line_surface, (x, y))

    return frame_surface
