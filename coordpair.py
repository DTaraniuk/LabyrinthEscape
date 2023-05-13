class CoordPair:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other: 'CoordPair'):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def to_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def __iter__(self):
        return iter((self.x, self.y))

    def equals(self, other: 'CoordPair') -> bool:
        return (self.x, self.y) == (other.x, other.y)
