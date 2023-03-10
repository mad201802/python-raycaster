from tkinter import Tk, Canvas, Frame, BOTH, Toplevel
from ray import Ray, Vec2
from boundary import Boundary
from origin import RaycastOrigin

import utils

WIDTH = 1600
HEIGHT = 900

class RaycasterWindow:

    def __init__(self, master):
        master.title("Raycaster")
        master.bind("<KeyPress>", self.on_key_press)

        self.frame = Frame(master)
        self.frame.pack()

        self.render_view = RenderView()

        self.canvas = None
        self.boundaries: list[Boundary] = []
        self.raycast_origin = None

        self.initUI()

    def on_key_press(self, event):
        self.canvas.delete("ray")
        self.canvas.delete("intersect")

        if event.char == 'a':
            self.raycast_origin.rotate(-1.0)
        elif event.char == 'd':
            self.raycast_origin.rotate(1.0)

        self.raycast_origin.update_rays()
        self.raycast_origin.draw()
        
        distances = self.raycast_origin.intersect(self.boundaries)

        self.render_view.update(distances)

    def onMouseMove(self, event):
        mouse_x = event.x
        mouse_y = event.y

        self.canvas.delete("ray")
        self.canvas.delete("intersect")

        self.raycast_origin.origin = Vec2(mouse_x, mouse_y)

        self.raycast_origin.update_rays()
        self.raycast_origin.draw()
        
        distances = self.raycast_origin.intersect(self.boundaries)

        self.render_view.update(distances)

    def initUI(self):
        self.canvas = Canvas(self.frame, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.bind("<Motion>", self.onMouseMove)

        self.boundaries.append(Boundary(Vec2(0, 0), Vec2(WIDTH, 0)))
        self.boundaries.append(Boundary(Vec2(WIDTH, 0), Vec2(WIDTH, HEIGHT)))
        self.boundaries.append(Boundary(Vec2(WIDTH, HEIGHT), Vec2(0, HEIGHT)))
        self.boundaries.append(Boundary(Vec2(0, HEIGHT), Vec2(0, 0)))

        self.boundaries.append(Boundary(Vec2(1000, 200), Vec2(1000, 700)))
        self.boundaries.append(Boundary(Vec2(1300, 50), Vec2(1300, 500)))
        self.boundaries.append(Boundary(Vec2(500, 400), Vec2(300, 500)))

        for b in self.boundaries:
            b.draw(self.canvas)

        self.raycast_origin = RaycastOrigin(self.canvas, Vec2(WIDTH/2, HEIGHT/2))

        self.canvas.pack(fill=BOTH, expand=1)

class RenderView:
    def __init__(self):
        self.frame = Frame(Toplevel(width=WIDTH, height=HEIGHT), width=WIDTH, height=HEIGHT)
        self.frame.pack()

        self.canvas = None

        self.initUI()

    def initUI(self):
        self.canvas = Canvas(self.frame, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack(fill=BOTH, expand=1)

    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb 

    def update(self, data: list[float]):
        # show a label with current value
        self.canvas.delete("all")

        width = WIDTH / len(data)
        for i, d in enumerate(data):
            x1 = i * width
            y1 = utils.map(d, 0, WIDTH, 0, HEIGHT/2)
            x2 = x1 + width
            y2 = HEIGHT - y1

            data_squared = d * d
            width_squared = WIDTH * WIDTH

            raw_color = utils.map(data_squared, 0, width_squared, 255, 0) if d < float("inf") else 0
            color = int(raw_color)

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self._from_rgb((color, color, color)), outline=self._from_rgb((color, color, color)))

def main():

    root = Tk()
    window = RaycasterWindow(root)

    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.mainloop()


if __name__ == '__main__':
    main()