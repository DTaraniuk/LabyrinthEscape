import pygame
from typing import Optional
from game_logic.coordpair import CoordPair


class Circle:
    def __init__(self,
                 x: float,
                 y: float,
                 radius: float):
        self.center = CoordPair(x, y)
        self.radius = radius

    # returns the point of other where the collision happened
    def collide(self, other) -> Optional[CoordPair]:
        if isinstance(other, Circle):
            return self._collide_circle(other)
        elif isinstance(other, pygame.Rect):
            return self._collide_rect(other)

    def _collide_circle(self, other: 'Circle') -> Optional[CoordPair]:
        o_o1 = (self.center - other.center)
        dist_sq = o_o1.x ** 2 + o_o1.y ** 2
        if dist_sq > (self.radius + other.radius)**2:
            return None
        collision_point = other.center - o_o1.normalize() * other.radius
        return collision_point

    def _collide_rect(self, rect: pygame.Rect) -> Optional[CoordPair]:
        circle_distance_x = abs(self.center.x - rect.centerx)
        circle_distance_y = abs(self.center.y - rect.centery)

        if circle_distance_x > (rect.w / 2 + self.radius):
            return None
        if circle_distance_y > (rect.h / 2 + self.radius):
            return None

        nearest_rect_horizontal_edge = rect.left if self.center.x < rect.centerx else rect.right
        nearest_rect_vertical_edge = rect.top if self.center.y < rect.centery else rect.bottom

        if circle_distance_x <= (rect.w / 2):
            # Collided with the top or bottom
            return CoordPair(self.center.x, nearest_rect_vertical_edge)
        if circle_distance_y <= (rect.h / 2):
            # Collided with the left or right
            return CoordPair(nearest_rect_horizontal_edge, self.center.y)

        # Collision with corner. Need to find the nearest corner
        closest_corner = CoordPair(nearest_rect_horizontal_edge, nearest_rect_vertical_edge)
        corner_distance_sq = (self.center.x - closest_corner.x) ** 2 + (self.center.y - closest_corner.y) ** 2

        if corner_distance_sq <= (self.radius ** 2):
            return closest_corner

        return None


