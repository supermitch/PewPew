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


class GameWorld(object):
    """ Game play contents """
    def __init__(self, size):
        w, h = size
        self.surfaces = []


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


class GameOverWorld(object):
    """ The surfaces of the Game Over scene. """

    def __init__(self, size, result):
        center_x = size[0] / 2
        center_y = size[1] / 2

        self.surfaces = []

        # Semi-transparent background
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((0, 0, 0, 200))
        pos = (0, 0)
        self.surfaces.append((surf, pos))

        surf = large.render("Game Over!", True, colors.fail)
        text_w, text_h = surf.get_size()
        pos = (center_x - text_w/2, center_y - text_h/2)
        self.surfaces.append((surf, pos))

        if result == 'infection':
            message = "The planet was infected... humanity is lost..."
        elif result == 'died':
            message = "You died. Earth's last line of defense has fallen..."
        else:
            message = 'Weird. Game ended.'

        surf = medium.render(message, True, colors.fail)
        text_w, text_h = surf.get_size()
        pos = (center_x - text_w/2, center_y - text_h/2 + 40)
        self.surfaces.append((surf, pos))

        surf = medium.render("Play again?", True, colors.plain)
        text_w, text_h = surf.get_size()
        pos = (center_x - text_w/2, center_y - text_h/2 + 80)
        self.surfaces.append((surf, pos))

        surf = medium.render("(Y)es         (N)o", True, colors.plain)
        text_w, text_h = surf.get_size()
        pos = (center_x - text_w/2, center_y - text_h/2 + 120)
        self.surfaces.append((surf, pos))

