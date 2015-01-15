import pygame
from pygame.locals import *

from screens.text import large, medium, small, colors

class StartWorld(object):
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

class VictoryWorld(object):
    """ Game victory surfaces. """

    def __init__(self, size):
        center_x = size[0] / 2
        center_y = size[1] / 2

        self.surfaces = []
        surf = large.render("You won!", True, colors.success)
        text_w, text_h = surf.get_size()
        pos = (center_x - text_w/2, center_y - text_h/2)
        self.surfaces.append((surf, pos))

        surf = medium.render("Play again?", True, colors.plain)
        text_w, text_h = surf.get_size()
        pos = (center_x - text_w/2, center_y - text_h/2 + 60)
        self.surfaces.append((surf, pos))

        surf = medium.render("(Y)es         (N)o", True, colors.plain)
        text_w, text_h = surf.get_size()
        pos = (center_x - text_w/2, center_y - text_h/2 + 100)
        self.surfaces.append((surf, pos))

