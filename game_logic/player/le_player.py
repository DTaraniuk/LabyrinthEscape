from common.constants import *
from game_logic.coordpair import CoordPair
from enum import Enum
from game_logic.player.modifier.le_modifier import LeModifier, LeModifierType
from game_logic.player.modifier.le__acceleration_modifier import LeAccelerationModifier
from typing import Union


class PlayerState(Enum):
    ALIVE = 'alive'
    ESCAPED = 'escaped'
    DEAD = 'dead'


class LePlayer:
    def __init__(self, pos: CoordPair, size: tuple[int, int], name: str = '',
                 alive_img=ALIVE_PLAYER_IMG, dead_img=DEAD_PLAYER_IMG, escaped_img=ESCAPED_PLAYER_IMG):
        self.name: str = name
        self._x: float = pos.x
        self._y: float = pos.y
        self.size = size
        self.speed = PLAYER_SPEED
        self.state: PlayerState = PlayerState.ALIVE
        self.move_direction: CoordPair = CoordPair()
        self._modifiers: dict[LeModifierType, list[LeModifier]] = {
            LeModifierType.Speed: [],
        }
        self.images: dict[PlayerState, str] = {PlayerState.ALIVE: alive_img,
                                               PlayerState.DEAD: dead_img,
                                               PlayerState.ESCAPED: escaped_img}

    @property
    def pos(self) -> CoordPair:
        return CoordPair(self._x, self._y)

    @pos.setter
    def pos(self, coords: CoordPair):
        if isinstance(coords, CoordPair):
            self._x = coords.x
            self._y = coords.y

    @property
    def center(self) -> CoordPair:
        size_x, size_y = self.size
        return CoordPair(self._x + size_x / 2, self._y + size_y / 2)

    @center.setter
    def center(self, value: Union[CoordPair, tuple[float, float]]):
        size_x, size_y = self.size
        if isinstance(value, CoordPair):
            self._x = value.x - size_x / 2
            self._y = value.y - size_y / 2
        elif isinstance(value, tuple):
            self._x = value[0] - size_x / 2
            self._y = value[1] - size_y / 2

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_image(self):
        return self.images[self.state]

    def move(self, ticks: int) -> CoordPair:
        x, y = self.center
        dx, dy = self.move_direction
        speed = self.speed
        speed_mods: list[LeModifier] = self._modifiers.get(LeModifierType.Speed)
        dest = CoordPair(x, y)
        for speed_mod in speed_mods:
            if isinstance(speed_mod, LeAccelerationModifier) and speed_mod.is_active:
                dest += speed_mod.move_dir * speed_mod.increase

        dest += CoordPair(dx * speed * ticks, dy * speed * ticks)
        return dest

    def add_modifier(self, modifier: LeModifier):
        self._modifiers[modifier.type].append(modifier)

    def update_modifiers(self, ticks: int):
        for mod_list in self._modifiers.values():
            for mod in mod_list:
                if not mod.is_active:
                    mod_list.remove(mod)
                mod.update(ticks)
