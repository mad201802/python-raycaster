import math

class Vec2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def get_normalized(self):
        return Vec2(self.x / abs(self.length()), self.y / abs(self.length()))
    
    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"
    
    def distance_to(self, other):
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y) ** 2)