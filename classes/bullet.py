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
            color = (220, 100, 100)
            self.width = 5
            self.height = 5
            self.strength = 15

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(color)

        self.x = shooter.rect.midtop[0] - (self.width / 2)
        self.y = shooter.rect.midtop[1]
        if direction != 'up':
            self.y = shooter.rect.center[1]

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if direction == 'up':
            self.speed_y = 40
            sign = 1 if shooter.speed > 0 else -1
            self.speed_x = sign * shooter.speed
        else:
            self.speed_y = 0
            sign = -1 if direction == 'left' else 1
            self.speed_x = int(sign * 15 + shooter.speed)

        self.dead = False

    def update(self):
        self.move()

    def move(self):
        self.rect.move_ip(self.speed_x, -self.speed_y)

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

