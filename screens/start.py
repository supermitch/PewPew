import pygame
from pygame.locals import *

from screens.text import large, medium, small, colors

class StartScreen(object):
    """ Game intro screen. """

    def __init__(self, size):
        w, h = size

        self.surfaces = []

        surf = large.render('PewPew', True, colors.bright)
        text_w, text_h = surf.get_size()
        pos = (w/2 - text_w/2, h/2 - text_h/2)
        self.surfaces.append((surf, pos))

        surf = medium.render('- Press spacebar to play -',
                             True, colors.plain)
        text_w, text_h = surf.get_size()
        pos = (w/2 - text_w/2, h/2 - text_h/2 + 60)
        self.surfaces.append((surf, pos))

