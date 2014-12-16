import pygame

class Wall(object):
    """ Left & right screen walls. """

    def __init__(self, left, screen_height):

        self.rect = pygame.Rect(left, -50, 50, screen_height + 100)
        self.strength = 0
        self.health = float("inf")
        # Used for momentum (rebound) calcs
        self.mass = 1e20  #float("inf")
        self.speed_x = 0
        self.speed_y = 0

    def collide(self, obj):
        """ React to collision. """
        pass

