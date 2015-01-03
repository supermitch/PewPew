import math
import random

import pygame

class Monster(object):

    def __init__(self, kind, surf, pos):
        self.surf = surf

        if kind == 'green':
            self.speed_x = 0
            self.speed_y = 1
            self.strength = 5
            self.health = 10
            self.mass = 10
        elif kind == 'red':
            self.speed_x = 0
            self.speed_y = 0.8
            self.strength = 10
            self.health = 30
            self.mass = 20
        elif kind == 'purple':
            self.speed_x = 0
            self.speed_y = 3
            self.strength = 2
            self.health = 10
            self.mass = 2
        elif kind == 'blue':
            self.speed_x = 0
            self.speed_y = 4
            self.strength = 1
            self.health = 10
            self.mass = 2
            self.rads = 0
            self.motion = sin_motion

        self.width, self.height = self.surf.get_size()

        self.x, self.y = pos

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.status = {}
        self.dead = False

    def update(self):
        self.check_status()
        if hasattr(self, 'motion'):
            self.motion(self)
        self.move()

    def collide(self, obj):
        """ Collide with an object. """
        self.damage(obj.strength)

    def move(self):
        """ Move our rectangle. """
        self.rect.move_ip(self.speed_x, self.speed_y)

    def damage(self, strength):
        """ Damage our object, kill it if zero health. """
        self.health = self.health - strength
        self.set_status('injured', 6)
        if self.health <= 0:
            self.dead = True

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

    def set_status(self, status, frame_count):
        """ Insert status for a certain number of frames. """
        self.status[status] = frame_count

    def check_status(self):
        """ Remove expired statuses, update others. """
        self.status = {k: v - 1 for k, v in self.status.items() if v > 0}

def sin_motion(self):
    self.rads = (self.rads + 0.1) % (2 * math.pi)
    self.speed_x = math.sin(self.rads) * 4

