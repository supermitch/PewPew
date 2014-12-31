from __future__ import division

import pygame
from pygame.locals import *

class Ship(object):

    def __init__(self, surf, pos):

        self.surf = surf
        self.width, self.height = self.surf.get_size()

        self.x, self.y = pos
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # TODO: Cheat mode w/ args?
        self.invincible = False  # Debug
        self.strength = 50
        self.max_health = 50.0
        self.health = 50.0
        self.dead = False
        self.exploded = False

        self.max_fuel = 400.0
        self.fuel_consumption = 0.0025  # Lower is better
        self.fuel = 400.0
        self.mass = 50.0

        self.thrusters = {'left': False, 'right': False, 'grav': False}
        self.thrust = 0  # Current thrust
        self.thrust_max = 80  # Thrust capability

        # TODO: Add anti-gravity, which allows frictionless sliding

        self.speed = 0.0  # Current speed
        self.max_speed = 12.0  # Speed capability

        self.mv = {'left':False, 'right':False, 'up':False, 'down':False}
        self.facing = {'west':False, 'east':False,
                       'north':True, 'south':False}

        self.status = {}

    @property
    def health_percentage(self):
        return self.health / self.max_health * 100.0

    @property
    def fuel_percentage(self):
        return self.fuel / self.max_fuel * 100.0

    def activate_thrusters(self, direction, switch=True):
        """ Adjust our thrust according to button press or release. """
        self.thrusters[direction] = switch

    def check_thrusters(self):
        if self.thrusters['left'] and not self.thrusters['right']:
            self.thrust = -1 * self.thrust_max
        elif self.thrusters['right'] and not self.thrusters['left']:
            self.thrust = self.thrust_max
        else:
            # Both thrusters cancel each other out
            self.thrust = 0

    def update(self):
        if not self.dead:
            self.check_status()
            self.check_thrusters()
            self.move()
            self.fuel -= abs(self.thrust) * self.fuel_consumption

    def friction(self):
        """ Calculate force of friction. """
        # Friction always opposes movement
        if self.speed > 0:
            direction = -1
        elif self.speed < 0:
            direction = 1
        else:
            # If we're not moving, we resist thrust
            if self.thrust > 0:
                direction = -1
            elif self.thrust < 0:
                direction = 1
            else:
                direction = 0

        if self.thrusters['grav']:  # Anti-grav is on
            mu = 0.0
        else:
            mu = 0.13  # TODO: Function of surface and ship attribs
        g = 9.8  # m/s^2 TODO: Function of planet
        return mu * self.mass * g * direction

    @property
    def acceleration(self):
        friction = self.friction()
        # Can't have more friction than thrust:
        if self.thrust > 0:
            friction = max(-1 * self.thrust, friction)
        elif self.thrust < 0:
            friction = min(-1 * self.thrust, friction)
        return (self.thrust + friction) / self.mass


    def set_speed(self, acceleration):
        """ Modify speed by acceleration. Limited to max_speed. """
        if not self.thrust:
            # Don't allow us to decelerate past a stop from friction
            if self.speed > 0 and acceleration < 0:
                self.speed = max(0, self.speed + acceleration)
            elif self.speed < 0 and acceleration > 0:
                self.speed = min(0, self.speed + acceleration)
        else:
            new_speed = self.speed + acceleration
            if self.speed <> 0:
                if cmp(self.speed, 0) <> cmp(new_speed, 0):  # same sign
                    self.speed = 0  # Pause at zero first
                else:
                    self.speed = new_speed
            else:
                self.speed = new_speed

        if abs(self.speed) >= self.max_speed:
            self.speed = self.speed / abs(self.speed) * self.max_speed

    def move(self):
        """ Update speed given acceleration and move ship accordingly. """
        self.set_speed(self.acceleration)
        # Save our position as a float to avoid integer step changes
        # when only using rect for positioning.
        self.x += self.speed
        self.rect.centerx = self.x

    def damage(self, strength):
        """
        Damage our object, kill it if zero health.

        strength is attacker's damage strength.

        """
        if strength > 0:  # TODO: defence could counter strength
            self.set_status('injured', 6)
        if not self.invincible:
            self.health -= strength
        if self.health <= 0:
            self.dead = True

    def collide(self, other, elasticity, reset):
        # this code assumes only some overlap, not total object crossing!
        if other.strength > 0:
            self.damage(other.strength)

        if reset:
            # Reset our position
            if other.rect.left < self.rect.left < other.rect.right:
                self.rect.left = other.rect.right
            elif other.rect.right > self.rect.right > other.rect.left:
                self.rect.right = other.rect.left
            self.x = self.rect.centerx  # Don't forget to update position, too!
        # http://en.wikipedia.org/wiki/Inelastic_collision
        self.speed = (0.9 * other.mass * (other.speed_x - self.speed) + \
            (self.mass * self.speed) + (other.mass * other.speed_x)) \
            / (self.mass + other.mass)

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

    def set_status(self, status, frame_count):
        """ Set a status for a given duration. """
        self.status[status] = frame_count

    def check_status(self):
        """ Check statuses to see if they have expired. """
        expired = []
        self.status = {k: v - 1 for k, v in self.status.items() if v > 0}

    def self_destruct(self):
        """ Damage by remaining health value, and die. """
        self.damage(self.health)

