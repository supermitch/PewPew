from __future__ import division
import random

import antigrav
import bullet
import explosion
import monster
import hero
import wall
import level

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
        self.antigrav = self.__add_antigrav()
        self.bullets = []
        self.monsters = []
        self.explosions = []

        self.ADD_MONSTER = 2.5
        self.last_add = 0

        self.level = None

    def load_level(self, level_number):
        self.level = level.levels[level_number - 1]  # zero index
        return self.level.total_monsters()

    def __add_hero(self, screen_size):
        """ Add our hero to bottom of the screen. """
        surf, size = self.assets.images['ship']
        x = (screen_size[0] / 2) - (size[0] / 2)
        y = screen_size[1] - (size[1] * 2)
        return hero.Ship(surf, pos=(x, y))

    def __add_antigrav(self):
        surf, size = self.assets.images['anti-grav']
        pos = self.hero.rect.midbottom
        return antigrav.Antigrav(surf, pos)

    def __add_monster(self, screen_size, kind=None, left=None):
        """ Add a monster to the screen. """
        monster_names = {
            'red': 'enemy_1',
            'purple': 'enemy_2',
            'green': 'enemy_3',
            'blue': 'enemy_4',
        }
        if kind is None:
            kind = random.choice(monster_names.keys())

        surf, size = self.assets.images[monster_names[kind]]

        # Position somewhere along the top of the screen
        if left is None:
            x = random.randint(20 + size[0], screen_size[0] - (20 + size[0]))
        else:
            x = left
        y = -50
        self.monsters.append(monster.Monster(kind, surf, (x, y)))

    def add_explosion(self, source, kind='default'):
        """
        Add an explosion to the screen.

        Source must have a .rect attribute.

        """
        image_name = {
            # kind: asset (name attrib, or file)
            'default': 'explode',
            # TODO: different hero explosion
            'hero': 'explode',
        }[kind]
        sprites, size = self.assets.images[image_name]
        x = source.rect.centerx - size[0]/2
        y = source.rect.centery - size[1]/2
        self.explosions.append(explosion.Explosion(sprites, (x, y)))

        # TODO: Sound manager!
        if kind == 'default':
            self.assets.sounds['explode'].play(maxtime=350)
        elif kind == 'hero':
            self.assets.sounds['hero-explode'].play()

    def update(self, time):

        if self.hero.dead:
            if not self.hero.exploded:
                self.hero.exploded = True
                self.add_explosion(self.hero, kind='hero')
        self.hero.update(time)
        self.antigrav.update(self.hero.rect.midbottom)

        self.bullets = [b for b in self.bullets if not b.dead]
        for b in self.bullets:
            b.update()

        if self.level.waves:
            wave = self.level.waves[0]
            if time > wave[0]:
                for x in wave[1]:
                    self.__add_monster(self.screen_size, kind=wave[2], left=x)
                self.level.waves.pop(0)  # Get rid of it.
                self.last_add = time  # Don't add randomly right after

        if (time - self.last_add) >= self.ADD_MONSTER:
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

