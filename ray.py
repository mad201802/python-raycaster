from vec2 import Vec2
from boundary import Boundary
from tkinter import Canvas
import math

class Ray():
    def __init__(self, origin: Vec2, angle: float):
        self.origin = origin
        self.direction = Vec2(math.cos(angle), math.sin(angle))

    def draw(self, canvas: Canvas):
        # TODO: For now on ray is casted 10 units away
        scalar = 10
        canvas.create_line(self.origin.x, self.origin.y, self.origin.x + (self.direction.x * scalar), self.origin.y + (self.direction.y * scalar), fill="red", tags="ray")

    def set_angle(self, angle):
        self.direction = Vec2(math.cos(angle), math.sin(angle))

    def intersects(self, b: Boundary):
        x1 = b.a.x
        y1 = b.a.y
        x2 = b.b.x
        y2 = b.b.y

        x3 = self.origin.x
        y3 = self.origin.y
        x4 = self.origin.x + self.direction.x
        y4 = self.origin.y + self.direction.y

        den = (x1 -x2) * (y3 - y4) - (y1 - y2) * (x3 -x4)
        if den == 0:
            return None
        
        t = ((x1 -x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 -x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if t > 0 and t < 1 and u > 0:
            return Vec2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        return None