from vec2 import Vec2
from tkinter import Canvas

class Boundary():
    def __init__(self, a: Vec2, b: Vec2):
        self.a = a
        self.b = b

    def draw(self, canvas: Canvas):
        canvas.create_line(self.a.x, self.a.y, self.b.x, self.b.y, fill="white", tags="boundary")