import random

import pygame

class Monster(object):

    def __init__(self, kind, surf, pos):
        self.surf = surf

        if kind == 'strong':
            self.speed_y = 1
            self.strength = 10
            self.health = 30
            self.mass = 20
        elif kind == 'fast':
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

    def update(self, time):
        self.check_status(time)
        self.move()

    def collide(self, obj):
        """ Collide with an object. """
        self.damage(obj.strength)
        #self.set_status('injured', time, 50)

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
        if self.health <= 0:
            self.dead = True

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

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



