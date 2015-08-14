import pygame
from pygame.locals import *

class Bomb(object):

    def __init__(self, surf, shooter):

        self.surf = surf
        self.width, self.height = self.surf.get_size()

        self.strength = 15
        self.mass = 15

        # TODO: Is there a positioning / rect bug here? Why is centerx our x?
        self.x = shooter.rect.centerx
        self.y = shooter.rect.midbottom[1]

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed = shooter.speed
        self.thrust = 0
        self.mu = 0.5

        self.exploding = False
        self.blast_radius = 0
        self.max_blast_radius = 100
        self.dead = False

    def update(self):
        self.move()
        if self.exploding:
            self.explode()

    def draw(self):
        """ Return an (image, position) tuple. """
        return self.surf, self.rect.topleft

    def explode(self):
        """ Expand then rapidly contract blast radius on collision. """
        if self.expanding and self.blast_radius < self.max_blast_radius:
            self.blast_radius += 5  # Slower expansion
        else:
            self.expanding = False
            self.blast_radius -= 40  # Rapid collapse
            if self.blast_radius < 0:
                self.dead = True  # Fully collapsed

    def collide(self, obj):
        self.exploding = True
        self.expanding = True

    def friction(self):
        """ Calculate force of friction. """
        # Friction always opposes movement or force
        if self.speed != 0:
            sign = -1 if self.speed > 0 else 1
        else:
            sign = -1 if self.thrust > 0 else 1 if self.thrust < 0 else 0

        g = 9.8  # m/s^2 TODO: Function of planet
        return self.mu * self.mass * g * sign

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

