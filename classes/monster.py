import random

import pygame
from pygame.locals import *

class Monster(object):

    def __init__(self, img, size, pos):
        if random.choice([True, False]):
            self.img = 'enemy_1'
            self.speed_y = 1
            self.strength = 10
            self.health = 50
            self.mass = 20
        else:
            self.img = 'enemy_2'
            self.speed_y = 3
            self.strength = 2
            self.health = 10
            self.mass = 2

        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.death = False

        self.x = random.randint(20 + self.width,
                                screen_size[0] - (20+self.width))
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed_x = 0

        self.mv = {'left':False, 'right':False, 'up':False, 'down':True}

        self.status = {}

    def update(self, time):
        self.check_status(time)
        self.move()

    def move(self):
        """ Movement... """
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
        if self.health <= 0:
            self.death = True

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.img, self.rect.topleft

    def set_status(self, status, time, duration):
        self.status[status] = (time, duration)

    def check_status(self, current_time):
        remove = []
        for key, (set_time, duration) in self.status.items():
            # If enough time has gone by, this status has ended
            if (current_time - set_time) > duration:
                remove.append(key)
        for key in remove:
            del self.status[key]



