import math


class CoordPair:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other: 'CoordPair'):
        x = self.x + other.x
        y = self.y + other.y
        return CoordPair(x, y)

    def __sub__(self, other: 'CoordPair'):
        x = self.x - other.x
        y = self.y - other.y
        return CoordPair(x, y)

    def __mul__(self, value):
        x = self.x * value
        y = self.y * value
        return CoordPair(x, y)

    def to_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def normalize(self) -> 'CoordPair':
        norma = math.sqrt(self.x ** 2 + self.y ** 2)
        if norma == 0:
            return CoordPair(0, 0)
        return CoordPair(self.x / norma, self.y / norma)

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return self.equals(other)

    def equals(self, other: 'CoordPair') -> bool:
        return (self.x, self.y) == (other.x, other.y)

    def clone(self):
        return CoordPair(self.x, self.y)

    def angle_between(self, other: 'CoordPair'):
        # calculate dot product
        dot_product = self.x * other.x + self.y * other.y

        # clamp dot_product in the interval [-1, 1]
        dot_product = max(-1.0, min(1.0, dot_product))

        # calculate angle in radians
        angle_rad = math.acos(dot_product)

        # convert angle to degrees
        angle_deg = math.degrees(angle_rad)

        return angle_deg

