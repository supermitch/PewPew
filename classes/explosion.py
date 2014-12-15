import math

import pygame

class Explosion(object):

    def __init__(self, sprites, pos):

        self.sprites = sprites
        self.surf = self.sprites[0]

        self.frame_count = 0
        self.complete = False

        self.x, self.y = pos
        self.rect = pygame.Rect(self.x, self.y, self.surf.get_width(),
                                 self.surf.get_height())

    def update(self):
        # Only update half a frame every game update
        self.frame_count += 1
        frame = int(math.floor(self.frame_count))
        if frame < 5:
            self.surf = self.sprites[frame]
        else:
            self.complete = True

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

