from __future__ import division
import math
from random import randint as ri, lognormvariate as lognorm

import pygame


class Star(object):

    def __init__(self, screen_size):
        screen_width, screen_height = screen_size
        pos = ri(5, screen_width), ri(5, screen_height)

        width = ri(1, 3)
        size = (width, width)
        self.rect = pygame.Rect(pos, size)
        self.color = (ri(100, 220), ri(100, 220), ri(100, 220))

        self.degrees = ri(0, 360)
        self.frequency = ri(0, 50)
        self.depth = ri(1, 20)

        self.frame_count = 0
        self.flicker_delay = ri(1, 180)  # Frames
        self.flickering = False

    def update(self):
        if not self.frequency:  # No flickering will occur anyway
            return

        if not self.flickering:
            if self.frame_count % self.flicker_delay == 0:
                self.flickering = True  # Start flickering
                self.frame_count = 0  # Restart counter
                self.flicker_delay = ri(1, 180)  # Different next time
        else:
            self.flicker()  # Update appearance
        self.frame_count += 1

    def flicker(self):
        self.degrees += self.frequency
        if min(self.degrees, 360) % 360 == 0:
            self.flickering = False  # Flicker complete
            self.degrees = 0  # Reset counter
            self.frequency = ri(0, 50)  # Random flicker rate
            self.depth = lognorm(1, 0) * 20  # Random flicker depth
        variation = math.cos(math.radians(self.degrees))
        new_color = tuple([max(0, min(c + variation * self.depth, 220)) for c in self.color])
        self.color = new_color


class Background(object):

    def __init__(self, screen_size):
        self.size = screen_size
        self.width, self.height = screen_size
        self.x, self.y = (0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surf = pygame.Surface(screen_size)
        self.stars = self._gen_stars()

    def _gen_stars(self):
        """ Place stars randomly on the screen. """
        return [Star(self.size) for _ in range(50, 200)]

    def update(self):
        """ Flicker colour and size. """
        for star in self.stars:
            star.update()
            pygame.draw.rect(self.surf, star.color, star.rect)

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

