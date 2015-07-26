from __future__ import division
import math
import random

import pygame

class Background(object):

    def __init__(self, screen_size):
        self.width, self.height = screen_size
        self.x, self.y = (0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surf = pygame.Surface(screen_size)
        self._gen_stars()

    def _gen_stars(self):
        ri = random.randint
        star_count = ri(50, 200)
        # Place stars randomly on the grid
        for _ in range(star_count):
            star_size = ri(1, 4)
            x = ri(5, self.width)
            y = ri(5, self.height)
            star_rect = pygame.Rect((x, y), (star_size, star_size))
            colour = (ri(200, 255), ri(200, 255), ri(200, 255))
            pygame.draw.rect(self.surf, colour, star_rect)

    def update(self):
        pass

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

