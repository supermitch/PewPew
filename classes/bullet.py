import pygame
from pygame.locals import *

class Bullet(object):

    def __init__(self, shooter):

        self.width = 3
        self.height = 3
        color = (220, 255, 255)

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(color)

        self.strength = 10

        self.x = shooter.rect.midtop[0] - (self.width / 2)
        self.y = shooter.rect.midtop[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed_y = 40
        self.speed_x = shooter.speed

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
            old_bottom = self.rect.bottom
            self.rect.move_ip(0, -self.speed_y)
            trail_height = (old_bottom - self.rect.top)
            self.trail_rect = pygame.Rect(self.rect.topleft,
                                        (self.rect.width, trail_height))
        if self.mv['left'] or self.mv['right']:
            self.rect.move_ip(self.speed_x, 0)

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

    def collide(self, obj):
        # TODO: Persistent bullet types won't die!
        # Any collision kills the bullet
        self.dead = True

