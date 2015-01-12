from __future__ import division
import math
import random

import pygame

from planet import Planet

class Monster(object):

    def __init__(self, kind, surf, pos):
        self.surf = surf
        self.obstacle = False  # Doesn't persist as an obstacle
        self.landed = False  # Hasn't already landed
        self.infectious = True  # By default, can infect humans
        self.kind = kind

        if kind == 'green':
            self.speed_x = 0
            self.speed_y = 1
            self.strength = 5
            self.health = 10
            self.mass = 10
            self.infection = 2
        elif kind == 'red':
            self.speed_x = 0
            self.speed_y = 0.5
            self.strength = 10
            self.health = 30
            self.mass = 20
            self.infection = 20
        elif kind == 'purple':
            self.speed_x = 0
            self.speed_y = 3
            self.strength = 2
            self.health = 10
            self.mass = 2
            self.infection = 5
        elif kind == 'blue':
            self.speed_x = 0
            self.speed_y = 4
            self.strength = 1
            self.health = 10
            self.mass = 2
            self.rads = 0
            self.infection = 1
            self.motion = sin_motion
        elif kind == 'boulder':
            self.obstacle = True
            self.speed_x = 0
            self.speed_y = 2
            self.strength = 5
            self.health = 20
            self.mass = 20
            self.infection = 0
            self.rads_per_frame = random.choice((-1, 1)) * \
                                  random.randint(5, 10)/100
            self.theta = random.random() * 2 * math.pi
            self.rotation = rotation
            self.infectious = False

        self.width, self.height = self.surf.get_size()

        self.x, self.y = pos

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.status = {}
        self.dead = False

    def update(self):
        self.check_status()
        if hasattr(self, 'motion'):
            self.motion(self)
        if hasattr(self, 'rotation'):
            self.rotation(self)
        self.move()

    def collide(self, obj):
        """ Collide with an object. """
        if isinstance(obj, Planet):
            if self.obstacle:
                # We've touched down
                self.speed_x = 0
                self.speed_y = 0
                self.rads_per_frame = 0
            else:
                self.dead = True
        else:
            self.damage(obj.strength)

    def move(self):
        """ Move our rectangle. """
        # Update first so we can keep non-integer positions
        self.x, self.y = self.x + self.speed_x, self.y + self.speed_y
        self.rect.topleft = (self.x, self.y)

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
    """ Wave-like left & right motion. """
    self.rads = (self.rads + 0.1) % (2 * math.pi)
    self.speed_x = math.sin(self.rads) * 4

def rotation(self):
    """ Rotation. """
    self.theta = (self.theta + self.rads_per_frame) % (2.0 * math.pi)

