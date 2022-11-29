import pygame, pygame.gfxdraw, sys, ann
from pygame.locals import *

pygame.init()

screen_size = (1280, 720)
screen_vec = pygame.Vector2(screen_size[0], screen_size[1])
display_surf = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption('snake')

background_color = (255, 255, 255)

class blob:
    def __init__(self, pos, radius, color):
        self.pos = pos
        self.pos_prev = pos
        self.radius = radius
        self.color = color
        self.acceleration = pygame.Vector2(0, 0)

    def update(self, dt):
        pos_tmp = pygame.Vector2(self.pos.x, self.pos.y)
        self.pos = 2 * self.pos - self.pos_prev + self.acceleration * (dt ** 2)
        self.pos_prev = pos_tmp

    def get_pos(self, pos):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos
    
    def add_pos(self, pos):
        self.pos += pos

    def sub_pos(self, pos):
        self.pos -= pos

    def set_vel(self, vel):
        self.pos_prev = self.pos - vel

    def get_vel(self):
        return self.pos - self.pos_prev

    def draw(self):
        global display_surf
        pygame.gfxdraw.aacircle(display_surf, int(self.pos.x), int(self.pos.y), int(self.radius), self.color)

class snake:
    def __init__(self, pos, radius, color):
        self.body = []
        self.body.append(blob(pos, radius, color))
        self.head = self.body[0]
        self.radius = radius
        self.color = color

    def draw(self):
        for b in self.body:
            b.draw()

    def update(self, dt):
        default_len = self.radius * 2
        for i in range(1, len(self.body)):
            diff = self.body[i - 1].pos - self.body[i].pos
            diff_len = diff.magnitude()
            if diff_len > default_len:
                diff = diff.normalize()
                diff_factor = (diff_len - default_len) / diff_len * 20
                self.body[i].add_pos(diff * diff_factor)

    def grow(self):
        if len(self.body) > 1:
            dir_vec = (self.body[-2].pos - self.body[-1].pos).normalize()
            self.body.append(blob(self.body[-1].pos - dir_vec * self.radius * 2, self.radius, self.color))
        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dir_vec = (pygame.Vector2(mouse_x, mouse_y) - self.body[-1].pos).normalize()
            self.body.append(blob(self.body[-1].pos - dir_vec * self.radius * 2, self.radius, self.color))
            
default_radius = 10

things = []

things.append(snake(screen_vec * 0.5, default_radius, (255, 0, 0)))

while True:
    display_surf.fill(background_color)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for thing in things:
        thing.draw()
        thing.update(1 / fps)
    clock.tick(fps)
    pygame.display.update()