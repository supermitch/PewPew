import pygame
from pygame.locals import *

class Wall(object):
    """ Screen walls. """

    def __init__(self, left, screen_height):

        self.rect = pygame.Rect(left, -50, 50, screen_height + 100)
        self.strength = float("inf")
        self.mass = 1e20  #float("inf")
        self.health = float("inf")
        self.speed_x = 0
        self.speed_y = 0

