from common.constants import*
from .coordpair import CoordPair


class Player:
    def __init__(self, pos: CoordPair, size: tuple[int, int], name: str = '', alive_img=ALIVE_PLAYER_IMG, dead_img=DEAD_PLAYER_IMG):
        self.name: str = name
        self._x: float = pos.x
        self._y: float = pos.y
        self.size = size
        self.speed = PLAYER_SPEED
        self.is_alive = True
        self.move_direction: CoordPair = CoordPair()
        self.images: dict[str, str] = {ALIVE: alive_img, DEAD: dead_img}

    def get_image(self):
        if self.is_alive:
            return self.images[ALIVE]
        else:
            return self.images[DEAD]

    def set_pos(self, coords: CoordPair):
        self._x, self._y = coords

    def get_pos(self) -> CoordPair:
        return CoordPair(self._x, self._y)

    def center(self, x, y):
        size_x, size_y = self.size
        self._x = x - size_x / 2
        self._y = y - size_y / 2

    def get_center(self) -> CoordPair:
        size_x, size_y = self.size
        return CoordPair(self._x + size_x / 2, self._y + size_y / 2)
