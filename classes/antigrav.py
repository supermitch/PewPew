from __future__ import division
import math

import pygame

class Antigrav(object):

    def __init__(self, sprites, pos):
        """ Initialize with spritesheet and initial position. """
        self.sprites = sprites
        self.surf = self.sprites[0]

        self.frame_count = 0

        self.x, self.y = pos
        self.rect = pygame.Rect(pos, self.surf.get_size())

    def update(self, pos):
        """ Update our sprite frame and position. """
        # Only update every 4 update calls (1/4 animation speed)
        frames = 4
        frame = int(math.floor(self.frame_count / frames))
        self.surf = self.sprites[frame]
        if self.frame_count == frames * 2 - 1:
            self.frame_count = 0
        else:
            self.frame_count += 1

        self.move(pos)

    def move(self, pos):
        """ Move our position and rect. """
        self.x, self.y = pos[0] - self.surf.get_width() / 2.0, pos[1] - 2
        self.rect.topleft = self.x, self.y

    def draw(self):
        """ Return an (image, position) tuple to the renderer. """
        return self.surf, self.rect.topleft

