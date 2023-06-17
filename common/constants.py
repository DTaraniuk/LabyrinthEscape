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
WALL_WIDTH = 2
GRID_WIDTH = 1
GRID = False
IMG_FOLDER = 'img'
ALIVE = 'alive'
ALIVE_PLAYER_IMG = 'rat.png'
MINOTAUR_IMG = 'minotaur.png'
DEAD = 'dead'
DEAD_PLAYER_IMG = 'dead_rat.png'
FPS = 20
_secs_to_pass_cell = 0.5
PLAYER_SPEED = int(WIDTH/ROWS/FPS/_secs_to_pass_cell)
PLAYER_SPEED = PLAYER_SPEED if PLAYER_SPEED > 0 else 1  # for smoothness, this has to be int, but > 0 ofc
PLAYER_MEM_SIZE = 400
MINOTAUR_SPEED = PLAYER_SPEED/2
KILL_DIST = WIDTH/ROWS/3
# endregion

# region surfaces
SURFACE_MAIN = "main"
SURFACE_MAZE = "maze"
SURFACE_GRID = "grid"
SURFACE_PATH = "path"
SURFACE_TEXT = "text"
SURFACE_PLAY = "play"
# endregion

# region network signals
START = 'start'
# endregion
