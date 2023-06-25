import enum
from abc import ABC


class LeModifierType(enum.Enum):
    Speed = 'spd',


class LeModifier(ABC):
    def __init__(self, duration_ticks: int, mod_type: LeModifierType):
        self._duration: int = duration_ticks
        self.is_permanent = False
        self.is_active: bool = True if duration_ticks > 0 else False
        self.type: LeModifierType = mod_type

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if self.is_permanent:
            return
        self._duration = value
        if self._duration <= 0:
            self.is_active = False

    def update(self, ticks: int):
        if self.is_permanent:
            return
        self.duration -= ticks
