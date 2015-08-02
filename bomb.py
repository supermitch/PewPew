import pygame
from pygame.locals import *

class Bomb(object):

    def __init__(self, shooter, direction):

        self.width = 20
        self.height = 10
        self.strength = 15

        self.surf = pygame.Surface((self.width, self.height))
        color = (50, 50, 50)
        self.surf.fill(color)

        self.x = shooter.rect.midtop[0] - (self.width / 2)
        self.y = shooter.rect.midtop[1]

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed_y = 0
        sign = -1 if direction == 'left' else 1
        self.speed_x = int(sign * shooter.speed)

        self.dead = False

    def update(self):
        self.move()

    def move(self):
        self.rect.move_ip(self.speed_x, -self.speed_y)

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

    def collide(self, obj):
        # TODO: Persistent bullet types won't die!
        self.dead = True  # Any collision kills bullet

