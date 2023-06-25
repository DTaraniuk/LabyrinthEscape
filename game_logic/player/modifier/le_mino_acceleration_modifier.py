from .le_modifier import LeModifier, LeModifierType
from game_logic import CoordPair
from common.constants import FPS

acceleration_buff_duration = FPS*20


class LeMinoAccelerationModifier(LeModifier):
    def __init__(self, increase: float, mod_type: LeModifierType, direction: CoordPair):
        super().__init__(acceleration_buff_duration, mod_type)
        self.increase: float = increase
        self.move_dir: CoordPair = direction






