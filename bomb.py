import pygame
from pygame.locals import *

class Bomb(object):

    def __init__(self, shooter, direction):

        self.width = 20
        self.height = 10
        self.strength = 15

        self.surf = pygame.Surface((self.width, self.height))
        color = (50, 50, 50)
        self.surf.fill(color)

        self.x = shooter.rect.midtop[0] - (self.width / 2)
        self.y = shooter.rect.midtop[1]

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed_y = 0
        sign = -1 if direction == 'left' else 1
        self.speed_x = int(sign * shooter.speed)
        self.mu = 0.5

        self.dead = False

    def update(self):
        self.move()

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

    def collide(self, obj):
        # TODO: Persistent bullet types won't die!
        self.dead = True  # Any collision kills bullet

    def friction(self):
        """ Calculate force of friction. """
        # Friction always opposes movement or force
        if self.speed != 0:
            sign = -1 if self.speed > 0 else 1
        else:
            sign = -1 if self.thrust > 0 else 1 if self.thrust < 0 else 0

        mu = 0.0 if self.thrusters['grav'] else self.mu
        g = 9.8  # m/s^2 TODO: Function of planet
        return mu * self.mass * g * sign

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
        # Don't allow us to decelerate past a stop from friction
        if self.speed > 0 and acceleration < 0:
            self.speed = max(0, self.speed + acceleration)
        elif self.speed < 0 and acceleration > 0:
            self.speed = min(0, self.speed + acceleration)

    def move(self):
        """ Update speed given acceleration and move ship accordingly. """
        self.set_speed(self.acceleration)
        # Save our position as a float to avoid integer step changes
        # when only using rect for positioning.
        self.x += self.speed
        self.rect.centerx = self.x

