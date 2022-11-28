import pygame, pygame.gfxdraw, sys
from pygame.locals import *

pygame.init()

screen_size = (1024, 576)
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
        self.radius = radius
        self.color = color

    

while True:
    display_surf.fill(background_color)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(fps)