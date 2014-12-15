import random

import explosion
import monster
import ship

class World(object):
    """ A class to hold all the game elements. """

    def __init__(self, screen_size, assets):
        self.screen_size = screen_size
        self.assets = assets

        self.hero = self.__add_hero(self.screen_size)
        self.bullets = []
        self.monsters = []
        self.explosions = []

        self.ADD_MONSTER = 2000
        self.last_add = 0

    def __add_hero(self, screen_size):
        """ Add our hero to bottom of the screen. """
        surf, size = self.assets.images['ship']
        x = (screen_size[0] / 2) - (size[0] / 2)
        y = screen_size[1] - (size[1] * 2)
        return ship.Ship(surf, pos=(x, y))

    def __add_monster(self, screen_size):
        """ Add a monster to the screen. """
        kind = random.choice(['strong', 'fast'])

        if kind == 'strong':
            name = 'enemy_1'
        elif kind == 'fast':
            name = 'enemy_2'
        surf, size = self.assets.images[name]

        # Position somewhere along the top of the screen
        x = random.randint(20 + size[0], screen_size[0] - (20 + size[0]))
        y = 0
        self.monsters.append(monster.Monster(kind, surf, (x, y)))

    def add_explosion(self, source):
        """ Add an explosion to the screen. """
        kind = 'default'
        if kind == 'default':
            sprites, size = self.assets.images['explode']
            x = source.rect.centerx - size[0]/2
            y = source.rect.centery - size[1]/2
            self.explosions.append(explosion.Explosion(sprites, (x, y)))


    def update(self, time):
        if time - self.last_add < self.ADD_MONSTER:
            return None
        else:
            self.last_add = time
            self.__add_monster(self.screen_size)

