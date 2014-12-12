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
        self.fuel_consumption = 0.1  # Lower is better
        self.fuel = 400.0
        self.mass = 50.0
        self.accel = 0.0

        self.thrust = 0  # Current thrust
        self.thrust_max = 40  # Thrust capability

        # TODO: Add anti-gravity, which allows frictionless sliding

        self.speed = 0.0  # Current speed
        self.max_speed = 12.0  # Speed capability

        self.mv = {'left':False, 'right':False, 'up':False, 'down':False}
        self.facing = {'west':False, 'east':False,
                       'north':True, 'south':False}

        self.status = {}

    def update(self, time):
        self.check_status(time)
        self.move()

    @property
    def friction(self):
        """ Calculate force of friction. """
        vector = 1 if self.speed > 0 else -1
        mu = 0.05  # TODO: Function of surface and ship attribs!
        g = 9.8  # m/s^2 TODO: Function of planet
        if abs(self.speed) <= 0.001 * self.max_speed:
            return 0
        else:
            return mu * self.mass * g * vector

    @property
    def acceleration(self):
        self.fuel -= abs(self.thrust) * self.fuel_consumption
        return (self.thrust - self.friction) / self.mass

    def activate_thrusters(self, direction):
        if direction == 'left':
            self.thrust = -1 * self.thrust_max
        elif direction == 'right':
            self.thrust = self.thrust_max
        elif direction == 'off':
            self.thrust = 0
        else:
            self.thrust = 0  # log error: "Bad direction"

    def set_speed(self, accel):
        """ Modify speed by acceleration. Limited to max_speed. """
        self.speed += self.acceleration
        if abs(self.speed) >= self.max_speed:
            self.speed = self.speed / abs(self.speed) * self.max_speed

    def move(self):
        """ Update speed given acceleration and move ship accordingly. """
        self.set_speed(self.accel)
        self.rect.move_ip(self.speed, 0)

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


