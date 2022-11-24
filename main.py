import pygame, pygame.gfxdraw, sys, math
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
        self.length = 1
        self.limit_length = limit_length
        self.radius = 10
        self.color = (0, 255, 0)
        self.body = [blob(pos, self.radius, self.color, None, None)]
        self.acceleration = pygame.Vector2(0, 0)
        self.speed = 10
        self.follow_speed = 1
        self.direction = 0

    def set_direction(self, direction):
        self.direction = direction

    def add_direction(self, delta):
        self.direction += delta

    def update(self, delta_t):
        self.acceleration = pygame.Vector2(math.cos(self.direction), math.sin(self.direction)) * self.speed
        self.body[0].set_force(self.acceleration)
        self.body[0].update(delta_t)
        for i in range(1, len(self.body)):
            if (self.body[i - 1].pos - self.body[i].pos).magnitude_squared() > ((self.body[i - 1].radius + self.body[i].radius) ** 2):
                self.body[i].set_force((self.body[i - 1].pos - self.body[i].pos).normalize() * self.speed)
            elif (self.body[i - 1].pos - self.body[i].pos).magnitude_squared() > ((self.body[i - 1].radius + self.body[i].radius) ** 2):
                self.body[i].set_force((self.body[i - 1].pos - self.body[i].pos).normalize() * -1)
            self.body[i].update(delta_t)

    def grow(self):
        if len(self.body) > 1:
            self.body.append(blob(self.body[-1].pos + (self.body[-2].pos - self.body[-1].pos).normalize() * -self.radius * 2, self.radius, self.color, self.body[-1], None))
            self.body[-2].tail = self.body[-1]
        else:
            self.body.append(blob(self.body[-1].pos + pygame.Vector2(math.cos(self.direction), math.sin(self.direction)) * self.radius * -2, self.radius, self.color, self.body[-1], None))
            self.body[-2].tail = self.body[-1]

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
fps = 30
one_frame = 0.1# / fps

things = []
things.append(snake(pygame.Vector2(500, 375), 10))

while True:
    display_surf.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[K_SPACE]:
                things[0].grow()
            if pressed[K_LEFT]:
                print('a')
                things[0].add_direction(-math.pi* 2 * 0.25)
            if pressed[K_RIGHT]:
                things[0].add_direction(math.pi * 2 * 0.25)

    for thing in things:
        if type(thing) == snake:
            for i in range(0, len(thing.body)):
                x, y = thing.body[i].pos
                r = thing.body[i].radius
                c = thing.body[i].color
                pygame.gfxdraw.aacircle(display_surf, int(x), int(y), int(r), c)

        if type(thing) == food:
            x, y = thing.pos
            r = thing.radius
            c = thing.color
            pygame.gfxdraw.aacircle(display_surf, int(x), int(y), int(r), c)
    things[0].update(one_frame)
    pygame.display.update()
    fps_clock.tick(fps)