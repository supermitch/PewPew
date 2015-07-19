import pygame
from pygame.locals import *

class Bullet(object):

    def __init__(self, shooter, direction='up'):

        if direction == 'up':
            self.width = 3
            self.height = 4
            color = (220, 255, 255)
            self.strength = 10
        else:
            color = (220, 50, 50)
            self.width = 5
            self.height = 5
            self.strength = 15

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(color)

        self.x = shooter.rect.midtop[0] - (self.width / 2)
        self.y = shooter.rect.midtop[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if direction == 'up':
            self.speed_y = 40
            self.speed_x = shooter.speed
        else:
            self.speed_y = 0
            sign = {'left': -1, 'right': 1}[direction]
            self.speed_x = sign * 20 + shooter.speed

        self.dead = False
        self.mv = {'up': True}

        # inherit shooter's left & right velocity
        self.mv['right'] = False
        self.mv['left'] = False
        if shooter.speed > 0:
            self.mv['right'] = True
        elif shooter.speed < 0:
            self.mv['left'] = True

    def update(self):
        self.move()

    def move(self):
        if self.mv['up']:
            #old_bottom = self.rect.bottom
            self.rect.move_ip(0, -self.speed_y)
            #trail_height = (old_bottom - self.rect.top)
            #self.trail_rect = pygame.Rect(self.rect.topleft,
            #                            (self.rect.width, trail_height))
        if self.mv['left'] or self.mv['right']:
            self.rect.move_ip(self.speed_x, 0)

    @property
    def next_rect(self):
        """ Return the position we'll be next frame. """
        top = self.rect.top - self.speed_y
        return pygame.Rect((self.rect.left, top),
                           (self.rect.width, self.speed_y))

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

    def collide(self, obj):
        # TODO: Persistent bullet types won't die!
        self.dead = True  # Any collision kills bullet

