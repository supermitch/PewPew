import pygame
from pygame.locals import *

from screens.text import large, medium, small, COLOR

class StartScreen(object):
    """ Game intro screen. """

    def __init__(self, size):
        w, h = size

        self.surfaces = [
            (
             large.render("PewPew", True, COLOR['ivory']),
             (w/2 - surf.get_width()/2, h/2 - surf.get_height()/2)
            ),
            (
             medium.render("- Press spacebar to play -", True, COLOR['white']),
             (w/2 - surf.get_width()/2, h/2 - surf.get_height()/2 + 60)
            ),
        ]


