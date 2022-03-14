import pygame as pg
import math
import numpy as np

_BLACK = (0, 0, 0)
_DARK_GRAY = (40, 40, 40)
_GRAY = (100, 100, 100)
_WHITE = (255, 255, 255)

draw_speed = 60
clock = pg.time.Clock()


class Cube:
    def __init__(self, surface, color, position, rotation, scale):
        self.surface = surface

        self.color = color

        self.position = position
        self.rotation = rotation
        self.scale = scale

        # Relative to center-point
        self.edge_points = (
            # Top-left
            # Top-Right
            # Bottom-Left
            # Bottom-Right

            np.array([[self.position[0] - self.scale[0] / 2, self.position[1] - self.scale[1] / 2, self.position[2] - self.scale[2] / 2],
                      [self.position[0] + self.scale[0] / 2, self.position[1] - self.scale[1] / 2, self.position[2] - self.scale[2] / 2],
                      [self.position[0] - self.scale[0] / 2, self.position[1] + self.scale[1] / 2, self.position[2] - self.scale[2] / 2],
                      [self.position[0] + self.scale[0] / 2, self.position[1] + self.scale[1] / 2, self.position[2] - self.scale[2] / 2],

                      [self.position[0] - self.scale[0] / 2, self.position[1] - self.scale[1] / 2, self.position[2] / 2 + self.scale[2] / 2],
                      [self.position[0] + self.scale[0] / 2, self.position[1] - self.scale[1] / 2, self.position[2] / 2 + self.scale[2] / 2],
                      [self.position[0] - self.scale[0] / 2, self.position[1] + self.scale[1] / 2, self.position[2] / 2 + self.scale[2] / 2],
                      [self.position[0] + self.scale[0] / 2, self.position[1] + self.scale[1] / 2, self.position[2] / 2 + self.scale[2] / 2],])
        )

        self.rotate_x(90 - self.rotation[0])
        self.rotate_y(90 - self.rotation[1])
        self.rotate_z(90 - self.rotation[2])

    def rotate_z(self, degrees):
        for ind, _ in enumerate(self.edge_points):
            r_x = self.edge_points[ind, 0] - self.position[0]
            r_y = self.edge_points[ind, 1] - self.position[1]
            r = math.hypot(r_x, r_y)
            theta = math.atan2(r_y, r_x) + math.radians(degrees)

            self.edge_points[ind, 0] = self.position[0] + r * math.cos(theta)
            self.edge_points[ind, 1] = self.position[1] + r * math.sin(theta)

    def rotate_y(self, degrees):
        for ind, _ in enumerate(self.edge_points):
            r_x = self.edge_points[ind, 0] - self.position[0]
            r_z = self.edge_points[ind, 2] - self.position[2]
            r = math.hypot(r_x, r_z)
            theta = math.atan2(r_x, r_z) + math.radians(degrees)

            self.edge_points[ind, 0] = self.position[0] + r * math.cos(theta)
            self.edge_points[ind, 2] = self.position[2] + r * math.sin(theta)

    def rotate_x(self, degrees):
        for ind, _ in enumerate(self.edge_points):
            r_y = self.edge_points[ind, 1] - self.position[1]
            r_z = self.edge_points[ind, 2] - self.position[2]
            r = math.hypot(r_y, r_z)
            theta = math.atan2(r_y, r_z) - math.radians(degrees)

            self.edge_points[ind, 1] = self.position[1] + r * math.cos(theta)
            self.edge_points[ind, 2] = self.position[2] + r * math.sin(theta)


    def render_points(self, point_radius):
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[0, :2], self.edge_points[2, :2], 1)
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[2, :2], self.edge_points[3, :2], 1)
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[1, :2], self.edge_points[3, :2], 1)
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[0, :2], self.edge_points[1, :2], 1)

        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[4, :2], self.edge_points[6, :2], 1)
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[6, :2], self.edge_points[7, :2], 1)
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[5, :2], self.edge_points[7, :2], 1)
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[4, :2], self.edge_points[5, :2], 1)

        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[0, :2], self.edge_points[4, :2], 1)
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[1, :2], self.edge_points[5, :2], 1)
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[2, :2], self.edge_points[6, :2], 1)
        pg.draw.line(self.surface, (0, 0, 255), self.edge_points[3, :2], self.edge_points[7, :2], 1)

        for x, y, z in sorted(self.edge_points, key=lambda x:x[2]):
            pg.draw.circle(self.surface, np.interp([z, z, z], [-10, 10], [60, 255]), (x, y), point_radius)


def setup():
    display_width = 500
    display_height = 500

    pg.init()
    dis = pg.display.set_mode((display_width, display_height))
    pg.display.set_caption('Pseudo-3D')

    dis.fill(_BLACK)
    pg.display.update()

    loop(dis)

def loop(dis):
    running = True

    x = 0
    y = 0
    z = 0

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running=False

        dis.fill(_BLACK)

        pressed = pg.key.get_pressed()
        if pressed[pg.K_w]:
            y += 1
        if pressed[pg.K_s]:
            y -= 1
        if pressed[pg.K_d]:
            x += 1
        if pressed[pg.K_a]:
            x -= 1
        if pressed[pg.K_q]:
            z += 1
        if pressed[pg.K_e]:
            z -= 1

        cube = Cube(dis, _WHITE, (100, 100, 0), (x, y, z), (50, 50, 50))
        cube.render_points(3)

        clock.tick(draw_speed)

        pg.display.flip()
    pg.quit()

if __name__=='__main__':
    setup()