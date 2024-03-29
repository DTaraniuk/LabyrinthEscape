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
PLAYER_SPEED = WIDTH/ROWS/FPS/_secs_to_pass_cell
PLAYER_SPEED = PLAYER_SPEED if PLAYER_SPEED > 0 else 1
_secs_player_mem = 10
PLAYER_MEM_SIZE = FPS * _secs_player_mem
MINOTAUR_SPEED = PLAYER_SPEED * 2/3
KILL_DIST = WIDTH/ROWS/3
# endregion

# region graphics

PLAYER_NAME_FONT = pygame.font.Font(None, 18)  # Parameters are 'None' or a filename, and a size (in points)
# endregion

# region network signals
START = 'start'
# endregion
