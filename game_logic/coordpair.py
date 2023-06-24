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

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return self.equals(other)

    def equals(self, other: 'CoordPair') -> bool:
        return (self.x, self.y) == (other.x, other.y)

    def clone(self):
        return CoordPair(self.x, self.y)
