import math

import pygame

class Explosion(object):

    def __init__(self, sprites, pos):

        self.sprites = sprites
        self.x, self.y = pos

        self.frame = 0
        self.frame_count = 0
        self.frame_rate = 1  # 1 frame per loop

        surf = self.sprites[0]
        self.rect = pygame.Rect(self.x, self.y, surf.get_width(), surf.get_height())

        self.complete = False  # All done exploding

    def update(self):
        self.increment_frame()

    def increment_frame(self):
        self.frame_count += (1 / self.frame_rate)
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

