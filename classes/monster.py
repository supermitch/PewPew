import random

import pygame

class Monster(object):

    def __init__(self, kind, surf, pos):
        self.surf = surf

        if kind == 'green':
            self.speed_y = 2
            self.strength = 5
            self.health = 10
            self.mass = 10
        elif kind == 'red':
            self.speed_y = 1
            self.strength = 10
            self.health = 30
            self.mass = 20
        elif kind == 'purple':
            self.speed_y = 3
            self.strength = 2
            self.health = 10
            self.mass = 2
        elif kind == 'blue':
            self.speed_y = 3
            self.strength = 2
            self.health = 10
            self.mass = 2
        self.speed_x = 0

        self.width, self.height = self.surf.get_size()

        self.x, self.y = pos

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.status = {}
        self.dead = False

        self.mv = {'left':False, 'right':False, 'up':False, 'down':True}

    def update(self):
        self.check_status()
        self.move()

    def collide(self, obj):
        """ Collide with an object. """
        self.damage(obj.strength)

    def move(self):
        """ Move our rectangle. """
        if self.mv['left']:
            self.rect.move_ip(-self.speed_x, 0)
        elif self.mv['right']:
            self.rect.move_ip(self.speed_x, 0)
        if self.mv['up']:
            self.rect.move_ip(0, -self.speed_y)
        elif self.mv['down']:
            self.rect.move_ip(0, self.speed_y)

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



