import random

import pygame

class Planet(object):
    """ The surface of the planet. """

    def __init__(self, screen_size):
        self.rect = pygame.Rect(-50, screen_size[1] - 20,
                                screen_size[0] + 100, 100)
        self.strength = 0  # Do no damage
        self.health = float('inf')  # Infinite life
        self.mass = 1e20
        self.speed_x = 0
        self.speed_y = 0
        self.surf = self._render_surface()
        self.pos = (0, screen_size[1] - 50)

    def collide(self, obj):
        """ React to collision. """
        pass

    def _render_surface(self):
        """ Auto generate random planet surface. """
        max_height = 8
        cols = self.rect.width
        surf = pygame.Surface((cols, max_height))
        color = (100, 155, 133)
        for col in range(0, cols, 2):
            height = random.randint(0, max_height + 1)
            rect = pygame.Rect(col, max_height - height, 2, height)
            surf.fill(color, rect)
        return surf

    def draw(self):
        return self.surf, self.pos

