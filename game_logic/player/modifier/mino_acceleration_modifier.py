from .le_modifier import Modifier, ModifierType
from game_logic import CoordPair
from common.constants import FPS

_max_acc = 0.5
BUFF_DURATION = FPS*2
MAX_ANGLE = 10
SPEED_MULT = _max_acc/BUFF_DURATION


class MinoAccelerationModifier(Modifier):
    def __init__(self, direction: CoordPair):
        super().__init__(BUFF_DURATION, ModifierType.Speed)
        self.mult: float = SPEED_MULT
        self.move_dir: CoordPair = direction.normalize()






