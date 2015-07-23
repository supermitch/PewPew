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
        star_rect = pygame.Rect((300, 300), (40, 40))
        pygame.draw.rect(self.surf, (255, 100, 255), star_rect)

    def update(self):
        pass

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

