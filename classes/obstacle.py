import pygame

class Obstacle(object):
    """ An obstacle that blocks the ship's lateral movement. """

    def __init__(self, kind, surf, pos):
        self.surf = surf
        self.x, self.y = pos
        if kind == 'debris':
            self.strength = 5
            self.health = 20
            self.mass = 20

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

