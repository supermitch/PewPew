import pygame

class Planet(object):
    """ The surface of the planet. """

    def __init__(self, screen_size):

        self.rect = pygame.Rect(-50, screen_size[1] - 20,
                                screen_size[0] + 100, 100)
        self.strength = 0  # Do no damage
        self.health = float('inf')  # Infinite life
        self.mass = 1e20
        self.speed_x = 0
        self.speed_y = 0

    def collide(self, obj):
        """ React to collision. """
        pass

    # TODO: Draw the surface.

