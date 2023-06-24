import enum
from abc import ABC

DurationEternal = -100


class LeModifierType(enum.Enum):
    Speed = 'spd',


class LeModifier(ABC):
    def __init__(self, duration_ticks: int, mod_type: LeModifierType):
        self._duration: int = duration_ticks
        self.is_active: bool = True if duration_ticks > 0 else False
        self.type: LeModifierType = mod_type

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if self._duration == DurationEternal:
            return
        self._duration = value
        if self._duration <= 0:
            self.is_active = False

    def update(self, ticks: int):
        if self._duration == DurationEternal:
            return
        self.duration -= ticks
