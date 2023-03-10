from vec2 import Vec2
from ray import Ray
from tkinter import Canvas
from boundary import Boundary

import utils
import math

class RaycastOrigin():
    def __init__(self, canvas: Canvas, origin: Vec2):
        self.canvas = canvas
        self.origin = origin
        self.heading = 0

        self.rays: list[Ray] = []

        self.update_rays()

    def update_rays(self):
        self.rays = []
        fov = 30
        num_rays = 100
        step_size = fov / num_rays
        for i in range(num_rays):
            angle = utils.degree_to_radians((i * step_size) - (fov / 2) + self.heading)
            ray = Ray(self.origin, angle)
            self.rays.append(ray)


    def draw(self):
        for ray in self.rays:
            ray.draw(self.canvas)

    def rotate(self, angle):
        self.heading += angle

    def intersect(self, boundaries: list):
        distances = []

        for ray in self.rays:
            closest = None
            record = float('inf')

            for b in boundaries:
                intersection = ray.intersects(b)
                if intersection:
                    distance = self.origin.distance_to(intersection)
                    distance *= math.cos(utils.vec_to_radians(ray.direction) - utils.degree_to_radians(self.heading))
                    if distance < record:
                        record = distance
                        closest = intersection
            if closest:
                self.canvas.create_line(self.origin.x, self.origin.y, closest.x, closest.y, fill="white", tags="ray")
            
            distances.append(record)

        return distances