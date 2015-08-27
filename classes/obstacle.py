import math
import random

from classes.monster import Monster
from classes.monster import rotation


class Obstacle(Monster):
    def __init__(self, sprites, pos):
        super(Obstacle, self).__init__(sprites, pos)
        self.obstacle = True
        self.infection = 0
        self.infectious = False


class Debris(Obstacle):
    def __init__(self, sprites, pos):
        super(Debris, self).__init__(sprites, pos)
        self.speed_y = 2
        self.strength = 5
        self.health = 20
        self.mass = 20
        self.rads_per_frame = random.choice((-1, 1)) * \
                              random.randint(5, 10)/100
        self.theta = random.random() * 2 * math.pi
        self.rotation = rotation


class Meteor(Obstacle):
    def __init__(self, sprites, pos):
        super(Meteor, self).__init__(sprites, pos)
        self.speed_y = 5
        self.strength = 10
        self.health = 50
        self.mass = 50


class Driller(Obstacle):
    def __init__(self, sprites, pos):
        super(Driller, self).__init__(sprites, pos)
        self.speed_y = 2
        self.strength = 10
        self.health = 50
        self.mass = 50

