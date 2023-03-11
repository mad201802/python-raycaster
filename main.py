import pygame as pg
import sys
import math

# Height and Width of screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BG_COLOR = (0, 0, 0)

GAME_MAP = [
    "####################",
    "#.................#",
    "#..1...1..........#",
    "#..1...1..........#",
    "#..1...1..........#",
    "#..11111..........#",
    "#.................#",
    "#.................#",
    "#.................#",
    "#.................#",
    "#.................#",
    "#.................#",
    "#.................#",
    "#.................#",
    "#.................#",
    "#.................#",
    "#...22.......22...#",
    "#...22.......22...#",
    "#.................#",
    "####################",
]

def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pg.display.set_caption("Move It!")
    pos_x, pos_y = 10, 10
    dir_x, dir_y = -1.0, 0.0
    plane_x, plane_y = 0.0, 0.66

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill(BG_COLOR)
       
        # Loop over all pixels in the screen
        for x in range(SCREEN_WIDTH):
            camera_x = 2.0 * x / SCREEN_WIDTH - 1.0
            ray_dir_x = dir_x + plane_x * camera_x
            ray_dir_y = dir_y + plane_y * camera_x

            map_x = int(pos_x)
            map_y = int(pos_y)

            delta_dist_x = math.sqrt(1 + (ray_dir_y * ray_dir_y) / (ray_dir_x * ray_dir_x)) if ray_dir_x != 0.0 else 1e30
            delta_dist_y = math.sqrt(1 + (ray_dir_x * ray_dir_x) / (ray_dir_y * ray_dir_y)) if ray_dir_y != 0.0 else 1e30

            step_x, step_y = 0, 0
            side_dist_x, side_dist_y = 0, 0
            perp_wall_dist = 0

            if ray_dir_x < 0:
                step_x = -1
                side_dist_x = (pos_x - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1.0 - pos_x) * delta_dist_x

            if ray_dir_y < 0:
                step_y = -1
                side_dist_y = (pos_y - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y + 1.0 - pos_y) * delta_dist_y

            hit = 0
            side = 0

            while hit == 0:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1

                if GAME_MAP[map_x][map_y] in ["#", "1", "2"]:
                    hit = 1
            
            if side == 0:
                perp_wall_dist = (map_x - pos_x + (1 - step_x) / 2) / ray_dir_x
            else:
                perp_wall_dist = (map_y - pos_y + (1 - step_y) / 2) / ray_dir_y

            line_height = int(SCREEN_HEIGHT / perp_wall_dist)

            draw_start = -line_height / 2 + SCREEN_HEIGHT / 2
            if draw_start < 0:
                draw_start = 0
            draw_end = line_height / 2 + SCREEN_HEIGHT / 2
            if draw_end >= SCREEN_HEIGHT:
                draw_end = SCREEN_HEIGHT - 1

            color = (255, 255, 255)
            if GAME_MAP[map_x][map_y] == "#":
                color = (255, 255, 255)
            elif GAME_MAP[map_x][map_y] == "1":
                color = (255, 0, 0)
            elif GAME_MAP[map_x][map_y] == "2":
                color = (0, 255, 0)

            pg.draw.line(screen, color, (x, draw_start), (x, draw_end))

        # Use keys to moce the player
        if pg.key.get_pressed()[pg.K_LEFT]:
            old_dir_x = dir_x
            dir_x = dir_x * math.cos(0.1) - dir_y * math.sin(0.1)
            dir_y = old_dir_x * math.sin(0.1) + dir_y * math.cos(0.1)
            old_plane_x = plane_x
            plane_x = plane_x * math.cos(0.1) - plane_y * math.sin(0.1)
            plane_y = old_plane_x * math.sin(0.1) + plane_y * math.cos(0.1)
        if pg.key.get_pressed()[pg.K_RIGHT]:
            old_dir_x = dir_x
            dir_x = dir_x * math.cos(-0.1) - dir_y * math.sin(-0.1)
            dir_y = old_dir_x * math.sin(-0.1) + dir_y * math.cos(-0.1)
            old_plane_x = plane_x
            plane_x = plane_x * math.cos(-0.1) - plane_y * math.sin(-0.1)
            plane_y = old_plane_x * math.sin(-0.1) + plane_y * math.cos(-0.1)
        if pg.key.get_pressed()[pg.K_UP]:
            if GAME_MAP[int(pos_x + dir_x * 0.1)][int(pos_y)] == ".":
                pos_x += dir_x * 0.1
            if GAME_MAP[int(pos_x)][int(pos_y + dir_y * 0.1)] == ".":
                pos_y += dir_y * 0.1
        if pg.key.get_pressed()[pg.K_DOWN]:
            if GAME_MAP[int(pos_x - dir_x * 0.1)][int(pos_y)] == ".":
                pos_x -= dir_x * 0.1
            if GAME_MAP[int(pos_x)][int(pos_y - dir_y * 0.1)] == ".":
                pos_y -= dir_y * 0.1

        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()