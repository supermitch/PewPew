import random

import bullet
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

        self.hero.update(time)

        for b in self.bullets:
            b.update()

        if (time - self.last_add) >= self.ADD_MONSTER:
            self.last_add = time
            self.__add_monster(self.screen_size)

        for m in self.monsters:
            m.update(time)

        for e in self.explosions:
            e.update()
        self.explosions = [e for e in self.explosions if not e.complete]


    def hero_shoot(self):
        # Limit firing rate, should be done by hero?
        if len(self.bullets) < 2:
            self.assets.sounds['shot'].play()
            self.bullets.append(bullet.Bullet(self.hero))
            self.stats['bullets_fired'] += 1

