import pygame
from pygame.locals import *

class Explosion(object):
    
    def __init__(self, source, image_list):

        self.explosion = image_list
        self.frame = 0
        self.complete = False
        self.img = self.explosion[self.frame]
        self.x = source.rect.centerx - self.img.get_width()/2
        self.y = source.rect.centery - self.img.get_height()/2
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(),
                                 self.img.get_height())
        self.rect.center = source.rect.center

    def update(self):
        self.frame += 1
        if self.frame < 5:
            self.img = self.explosion[self.frame]
        else:
            self.complete = True

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.img, self.rect.topleft

