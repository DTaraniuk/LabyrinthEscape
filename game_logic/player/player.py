from common.constants import *
from game_logic.coordpair import CoordPair
from enum import Enum
from game_logic.player.modifier.le_modifier import Modifier, ModifierType
from game_logic.player.modifier.mino_acceleration_modifier import MinoAccelerationModifier
from typing import Union, Iterable
from game_logic.circle import Circle
from game_logic.material_object import IMaterialObject


class PlayerState(Enum):
    ALIVE = 'alive'
    ESCAPED = 'escaped'
    DEAD = 'dead'


class Player(IMaterialObject):
    def __init__(self,
                 pos: Union[CoordPair, tuple[float, float]],
                 radius: float,
                 name: str = '',
                 alive_img=ALIVE_PLAYER_IMG,
                 dead_img=DEAD_PLAYER_IMG,
                 escaped_img=ESCAPED_PLAYER_IMG):
        self.name: str = name
        if isinstance(pos, CoordPair):
            pos = pos.to_tuple()
        x, y = pos
        self.area = Circle(x, y, radius)
        self.speed = PLAYER_SPEED
        self.state: PlayerState = PlayerState.ALIVE
        self._move_direction: CoordPair = CoordPair()
        self._modifiers: dict[ModifierType, list[Modifier]] = {
            ModifierType.Speed: [],
        }
        self.images: dict[PlayerState, str] = {PlayerState.ALIVE: alive_img,
                                               PlayerState.DEAD: dead_img,
                                               PlayerState.ESCAPED: escaped_img}

    def get_area(self):
        return self.area

    @property
    def center(self) -> CoordPair:
        return CoordPair(self.area.center.x, self.area.center.y)

    @center.setter
    def center(self, value: Union[CoordPair, tuple[float, float]]):
        self.area.center.x, self.area.center.y = value

    @property
    def move_direction(self):
        return self._move_direction

    @move_direction.setter
    def move_direction(self, value: CoordPair):
        self._move_direction = value.normalize()

    def get_image_name(self):
        return self.images[self.state]

    def get_move_vector(self, ticks: int) -> CoordPair:
        dx, dy = self.move_direction
        speed = self.speed
        speed_mods: list[Modifier] = self._modifiers.get(ModifierType.Speed)
        vec = CoordPair(0, 0)
        for speed_mod in speed_mods:
            if isinstance(speed_mod, MinoAccelerationModifier) and speed_mod.is_active:
                vec += speed_mod.move_dir * self.speed*speed_mod.mult

        vec += CoordPair(dx * speed * ticks, dy * speed * ticks)
        return vec

    def move(self, vector: CoordPair = None, ticks: int = None) -> CoordPair:
        if not vector:
            vector = self.get_move_vector(ticks)
        self.area.center += vector
        return vector

    # return: if the collision happened; adjusts position to avoid it
    def collide(self, other: IMaterialObject) -> bool:
        collide_point = self.area.collide(other.get_area())

        if collide_point:
            # put the player where he won't collide
            self.area.center = collide_point + (self.area.center - collide_point).normalize() * self.area.radius
            return True

        return False

    def add_modifier(self, modifier: Modifier):
        self._modifiers[modifier.type].append(modifier)

    def add_modifiers(self, modifiers: Iterable[Modifier]):
        for modifier in modifiers:
            self.add_modifier(modifier)

    def get_modifiers(self) -> list[Modifier]:
        modifiers: list[Modifier] = []
        for mod_list in self._modifiers.values():
            modifiers.extend(mod_list)
        return modifiers

    def update_modifiers(self, ticks: int):
        for mod_list in self._modifiers.values():
            for mod in mod_list:
                mod.update(ticks)
                if not mod.is_active:
                    mod_list.remove(mod)
