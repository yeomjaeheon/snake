import pygame, pygame.gfxdraw, sys
from pygame.locals import *

class blob:
    def __init__(self, pos, radius, color, head, tail):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.head = head
        self.tail = tail
        self.acceleration = pygame.Vector2(0, 0)
        self.prev_pos = [pos for i in range(0, 2)]


    def add_force(self, force):
        self.acceleration += force

    def set_force(self, force):
        self.acceleration = force

    def update(self, delta_t):
        self.prev_pos.append(self.prev_pos[-1] * 2 - self.prev_pos[-2] + self.acceleration * (delta_t ** 2))
        self.pos = self.prev_pos[-1]
        del self.prev_pos[0]

class snake:
    def __init__(self, pos, limit_length):
        self.head_pos = pos
        self.pos = [self.head_pos]
        self.length = 1
        self.limit_length = limit_length

class food:
    def __init__(self, pos, radius, color = (255, 0, 0)):
        self.pos = pos
        self.radius = radius
        self.color = color

pygame.init()

screen_size = (1000, 750)
world_size = (1000, 750)
display_surf = pygame.display.set_mode(screen_size)
pygame.display.set_caption('snake')
fps_clock = pygame.time.Clock()
fps = 60
one_frame = 1 / fps

things = []
things.append(food(pygame.Vector2(500, 375), 10))

while True:
    display_surf.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for thing in things:
        if type(thing) == blob:
            x, y = thing.pos
            r = thing.radius
            c = thing.color
            pygame.gfxdraw.aacircle(display_surf, int(x), int(y), int(r), c)

        if type(thing) == food:
            x, y = thing.pos
            r = thing.radius
            c = thing.color
            pygame.gfxdraw.aacircle(display_surf, int(x), int(y), int(r), c)
    pygame.display.update()
    fps_clock.tick(fps)