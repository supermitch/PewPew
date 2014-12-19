from __future__ import division
import random

import bullet
import explosion
import monster
import hero
import wall

class World(object):
    """ A class to hold all the game elements. """

    def __init__(self, screen_size, assets):
        self.screen_size = screen_size
        self.assets = assets

        self.walls = [
            wall.Wall(-50, self.screen_size[0]),
            wall.Wall(self.screen_size[0], self.screen_size[1])
        ]

        self.hero = self.__add_hero(self.screen_size)
        self.bullets = []
        self.monsters = []
        self.explosions = []

        self.ADD_MONSTER = 2.5
        self.last_add = 0
        # TODO: Move to level object?
        self.first_wave = False
        self.second_wave = False

    def __add_hero(self, screen_size):
        """ Add our hero to bottom of the screen. """
        surf, size = self.assets.images['ship']
        x = (screen_size[0] / 2) - (size[0] / 2)
        y = screen_size[1] - (size[1] * 2)
        return hero.Ship(surf, pos=(x, y))

    def __add_monster(self, screen_size, kind=None, left=None):
        """ Add a monster to the screen. """
        if kind is None:
            kind = random.choice(['strong', 'fast'])

        if kind == 'strong':
            name = 'enemy_1'
        elif kind == 'fast':
            name = 'enemy_2'
        surf, size = self.assets.images[name]

        # Position somewhere along the top of the screen
        if left is None:
            x = random.randint(20 + size[0], screen_size[0] - (20 + size[0]))
        else:
            x = left
        y = -50
        self.monsters.append(monster.Monster(kind, surf, (x, y)))

    def add_explosion(self, source):
        """ Add an explosion to the screen. """
        kind = 'default'
        if kind == 'default':
            sprites, size = self.assets.images['explode']
            x = source.rect.centerx - size[0]/2
            y = source.rect.centery - size[1]/2
            self.explosions.append(explosion.Explosion(sprites, (x, y)))
            self.assets.sounds['explode'].play(maxtime=350)

    def update(self, time):

        if self.hero.dead:
            self.add_explosion(m)
            self.assets.sounds['explode'].play()
        self.hero.update(time)

        self.bullets = [b for b in self.bullets if not b.dead]
        for b in self.bullets:
            b.update()

        if not self.first_wave and time > 5:
            self.last_add = time  # Don't add another randomly too soon
            left = range(300, 401, 40)
            for x in left:
                self.__add_monster(self.screen_size, kind='fast', left=x)
            self.first_wave = True
        elif not self.second_wave and time > 10:
            self.last_add = time
            left = range(200, 600, 100)
            for x in left:
                self.__add_monster(self.screen_size, kind='strong', left=x)
            self.second_wave = True
        elif (time - self.last_add) >= self.ADD_MONSTER:
            self.last_add = time
            self.__add_monster(self.screen_size)

        self.monsters = [m for m in self.monsters if not m.dead]
        for m in self.monsters:
            m.update(time)

        self.explosions = [e for e in self.explosions if not e.complete]
        for e in self.explosions:
            e.update()


    def hero_shoot(self):
        # Limit firing rate, should be done by hero?
        if len(self.bullets) < 2:
            self.assets.sounds['shot'].play()
            self.bullets.append(bullet.Bullet(self.hero))
            self.stats['bullets_fired'] += 1

