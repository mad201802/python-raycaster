from tkinter import Tk, Canvas, Frame, BOTH
from ray import Ray, Vec2
from boundary import Boundary
from origin import RaycastOrigin

WIDTH = 1600
HEIGHT = 900

class RaycasterWindow(Frame):

    def __init__(self):
        super().__init__()
        self.canvas = None
        self.boundaries: list[Boundary] = []
        self.raycast_origin = None

        self.initUI()

    def onMouseMove(self, event):
        mouse_x = event.x
        mouse_y = event.y

        self.canvas.delete("ray")
        self.canvas.delete("intersect")

        self.raycast_origin.origin = Vec2(mouse_x, mouse_y)

        self.raycast_origin.update_rays()
        self.raycast_origin.draw()
        
        self.raycast_origin.intersect(self.boundaries)


    def initUI(self):
        self.master.title("Raycaster")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.bind("<Motion>", self.onMouseMove)

        self.boundaries.append(Boundary(Vec2(1000, 200), Vec2(1000, 700)))
        self.boundaries.append(Boundary(Vec2(500, 400), Vec2(300, 500)))

        for b in self.boundaries:
            b.draw(self.canvas)

        self.raycast_origin = RaycastOrigin(self.canvas, Vec2(WIDTH/2, HEIGHT/2))

        self.canvas.pack(fill=BOTH, expand=1)

def main():

    root = Tk()
    RaycasterWindow()

    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.mainloop()


if __name__ == '__main__':
    main()