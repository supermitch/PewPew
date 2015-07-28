from __future__ import division
import math
from random import randint as ri

import pygame

class Star(object):

    def __init__(self, screen_size):
        screen_width, screen_height = screen_size
        pos = ri(5, screen_width), ri(5, screen_height)

        width = ri(1, 4)
        size = (width, width)
        self.rect = pygame.Rect(pos, size)
        self.color = (ri(150, 255), ri(150, 255), ri(150, 255))


class Background(object):

    def __init__(self, screen_size):
        self.size = screen_size
        self.width, self.height = screen_size
        self.x, self.y = (0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surf = pygame.Surface(screen_size)
        self.stars = self._gen_stars()
        self.update()

    def _gen_stars(self):
        """ Place stars randomly on the screen. """
        return [Star(self.size) for _ in range(50, 200)]

    def update(self):
        """ Flicker colour and size. """
        self.surf.fill((0, 0, 0))
        for star in self.stars:
            # new_color = tuple([min(c + ri(-40, 40), 255) for c in colour])
            pygame.draw.rect(self.surf, star.color, star.rect)

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

