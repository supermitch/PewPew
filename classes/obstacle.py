import pygame

class Obstacle(object):
    """ An obstacle that blocks the ship's lateral movement. """

    def __init__(self, kind, surf, pos):
        self.surf = surf
        self.x, self.y = pos
        kinds = {
            'debris': {'strength': 5, 'health': 20, 'mass': 20},
            'meteor': {'strength': 15, 'health': 50, 'mass': 40},
            'wall': {'strength': 5, 'health': 80, 'mass': 200},
            'barrier': {'strength': 5, 'health': 200, 'mass': 800},
            'shield': {'strength': 500, 'health': 2000, 'mass': 10000},
        }
        for property, value in kinds.get(kind).items():
            setattr(self, property, value)

        self. width, self.height = self.surf.get_size()

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed_x = 0.0
        self.status = {}
        self.dead = False

    def update(self):
        self.check_status()

    def collide(self, obj):
        """ Collide with an object. """
        self.damage(obj.strength)

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

