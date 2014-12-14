import ship
import monster

class World(object):
    """ A class to hold all the game elements. """

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.hero = ship.Ship(screen_size)
        self.bullets = []
        self.monster = []
        self.explosions = []
        self.frame_counter = 0
        self.ADD_MONSTER = 1000
        self.last_add = None

    def update(self, time):
        if self.last_add is not None:
            if time - self.last_add < self.ADD_MONSTER:
                return None
            else:
                self.last_add = None
        else:
            m = monster.Monster(self.screen_size, self.image_set)
            self.monsters.append(m)
            self.last_add = time

