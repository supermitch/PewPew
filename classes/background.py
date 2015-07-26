from __future__ import division
import math
from random import randint as ri

import pygame

class Background(object):

    def __init__(self, screen_size):
        self.width, self.height = screen_size
        self.x, self.y = (0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surf = pygame.Surface(screen_size)
        self.stars = self._gen_stars()
        self.update()

    def _gen_stars(self):
        """ Place stars randomly on the screen. """
        stars = []
        for _ in range(ri(50, 200)):
            width = ri(1, 4)
            size = (width, width)
            pos = ri(5, self.width), ri(5, self.height)
            star_rect = pygame.Rect(pos, size)
            colour = (ri(150, 255), ri(150, 255), ri(150, 255))
            stars.append((star_rect, colour))
        return stars

    def update(self):
        """ Flicker colour and size. """
        self.surf.fill((0, 0, 0))
        for star_rect, colour in self.stars:
            new_color = tuple([min(c + ri(-40, 40), 255) for c in colour])
            pygame.draw.rect(self.surf, new_color, star_rect)

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

