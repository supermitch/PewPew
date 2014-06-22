import pygame
from pygame.locals import *

class Ship(object):
    
    def __init__(self, screen_size):

        self.img = pygame.image.load('images/ship.png')
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.x = (screen_size[0] / 2) - (self.width / 2)
        self.y = screen_size[1] - (self.height * 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.max_health = 50.0
        self.health = 50.0
        self.death = False

        self.max_fuel = 400.0
        self.fuel = 400.0
        self.mass = 10
        self.accel = 0
        self.ACCELERATION = 0.5
        self.speed = 0
        self.max_speed = 15
        self.mv = {'left':False, 'right':False, 'up':False, 'down':False}
        self.facing = {'west':False, 'east':False,
                       'north':True, 'south':False}

    def accelerate(self, direction):

        if direction == 'left':
            self.accel = -1 * self.ACCELERATION
        elif direction == 'right':
            self.accel = self.ACCELERATION
        elif direction == 'off':
            self.accel = 0
        else:
            # log error: "Bad acceleration"
            self.accel = 0
        # can't accelerate past max speed
        if (abs(self.speed) >= self.max_speed) \
            and ((self.speed < 0) == (self.accel < 0)):
            self.accel = 0

    def set_speed(self, accel):

        if self.accel != 0:
            self.fuel -= abs(self.accel) * 1.0
        
        self.speed += self.accel

    def move(self):

        self.set_speed(self.accel)

        self.rect.move_ip(self.speed, 0)
        if self.speed > 0:
            self.dir_ew = 'right'
        if self.speed < 0:
            self.dir_ew = 'left'    # East / West direction

    def damage(self, strength):
        """ Damage our object, kill it if zero health."""
        self.health = self.health - strength
        if self.health <= 0:
            self.death = True

    def collide(self, other, elasticity, reset):
        # this code assumes only some overlap, not total object crossing!
        if reset:
            if other.rect.left < self.rect.left < other.rect.right:
                self.rect.left = other.rect.right
            elif other.rect.right > self.rect.right > other.rect.left:
                self.rect.right = other.rect.left
        self.speed = (self.speed * (self.mass - other.mass) + \
                     2 * other.mass * other.speed_x) / \
                     (self.mass + other.mass)
        self.speed *= elasticity    # scale by elasticity

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.img, self.rect.topleft

