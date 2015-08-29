import math

import pygame

class Explosion(object):

    def __init__(self, sprites, pos):

        self.sprites = sprites
        self.x, self.y = pos

        self.frame = 0
        self.frame_count = 0
        self.frame_rate = 1.0  # 1 frame per loop

        self.rect = pygame.Rect(self.x, self.y, self.sprites[0].get_width(), self.sprites[0].get_height())

        self.complete = False  # All done exploding

    def update(self):
        self.increment_frame()

    def increment_frame(self):
        self.frame_count += (1.0 / self.frame_rate)
        self.frame = int(math.floor(self.frame_count))
        if self.frame >= len(self.sprites):
            self.frame = 0
            self.frame_count = 0
            self.complete = True
        return self.frame

    @property
    def surf(self):
        return self.sprites[self.frame]

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

