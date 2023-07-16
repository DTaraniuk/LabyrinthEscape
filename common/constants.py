import pygame

pygame.init()

# region colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
LIGHT_BLUE = (0, 128, 255)
PINK = (255, 0, 128)
GREY = (100, 100, 100)
TRANSPARENT = (0, 0, 0, 0)
# endregion

# region app params
EPS = 1e-10
ROWS = 10
RAND_WALL_COUNT = ROWS//2
FONT_SIZE = 30
WIDTH = 800
HEIGHT = WIDTH
CELL_WIDTH = WIDTH/ROWS
WALL_WIDTH = 2
GRID_WIDTH = 1
GRID = False

IMG_FOLDER = 'img'
ALIVE_PLAYER_IMG = 'rat.png'
ESCAPED_PLAYER_IMG = 'victorious_rat.png'
DEAD_PLAYER_IMG = 'dead_rat.png'
MINOTAUR_IMG = 'minotaur.png'

FPS = 60
_secs_to_pass_cell = 1
PLAYER_SPEED = CELL_WIDTH/FPS/_secs_to_pass_cell
_secs_player_mem = 10
PLAYER_MEM_SIZE = FPS * _secs_player_mem
MINOTAUR_SPEED = PLAYER_SPEED * 2/3
PLAYER_CIRCLE_RADIUS = CELL_WIDTH/6
MINOTAUR_CIRCLE_RADIUS = CELL_WIDTH/4
KILL_DIST = CELL_WIDTH/3
# endregion

# region graphics

PLAYER_NAME_FONT = pygame.font.Font(None, 18)  # Parameters are 'None' or a filename, and a size (in points)
PLAYER_CIRCLE_COLOR = BLUE
PLAYER_CIRCLE_WIDTH = 1
# endregion

# region network signals
START = 'start'
# endregion
