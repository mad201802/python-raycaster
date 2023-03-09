from vec2 import Vec2
from ray import Ray
from utils import degree_to_radians
from tkinter import Canvas
from boundary import Boundary

class RaycastOrigin():
    def __init__(self, canvas: Canvas, origin: Vec2):
        self.canvas = canvas
        self.origin = origin

        self.rays: list[Ray] = []

        self.update_rays()

    def update_rays(self):
        self.rays = []
        for i in range(10, 370, 10):
            self.rays.append(Ray(self.origin, degree_to_radians(i)))

    def draw(self):
        for ray in self.rays:
            ray.draw(self.canvas)

    def intersect(self, boundaries: list):
        for ray in self.rays:
            closest = None
            record = float('inf')

            for b in boundaries:
                intersection = ray.intersects(b)
                if intersection:
                    distance = self.origin.distance_to(intersection)
                    if distance < record:
                        record = distance
                        closest = intersection
            if closest:
                self.canvas.create_line(self.origin.x, self.origin.y, closest.x, closest.y, fill="white", tags="ray")