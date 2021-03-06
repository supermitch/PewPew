from __future__ import division
import random

from classes import (antigrav, bomb, bullet, explosion, hero, level, monster,
                     obstacle, wall, planet, background)

class World(object):
    """ A class to hold all the game elements. """

    def __init__(self, screen_size, assets):
        self.screen_size = screen_size
        self.assets = assets

        self.walls = [
            wall.Wall(-50, self.screen_size[0]),
            wall.Wall(self.screen_size[0], self.screen_size[1]),
        ]

        self.background = background.Background(self.screen_size)
        self.hero = self.__add_hero(self.screen_size)
        self.antigrav = self.__add_antigrav()
        self.planet = planet.Planet(self.screen_size)
        self.bullets = []
        self.bombs = []
        self.monsters = []
        self.explosions = []

        self.add_monster_trigger = 200  # frames
        self.add_count = 0

        self.stage_clear = False
        self.stage_start = False
        self.level = None  # The level instance
        self.waves = []  # We store a copy of level waves

        self.infection = 0.0

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

    def __add_monster(self, kind=None, left=None):
        """ Add a monster to the screen. """
        sprites = {
            'red': 'enemy_1',
            'purple': 'enemy_2',
            'green': 'enemy_3',
            'blue': 'enemy_4',
        }
        if kind is None or kind not in sprites:
            kind = random.choice(sprites.keys())

        sprite = sprites[kind]
        surf, size = self.assets.images[sprite]

        # Position somewhere along the top of the screen
        if left is None:
            x = random.randint(20 + size[0], self.screen_size[0] - (20 + size[0]))
        else:
            x = left
        y = -50
        monster_class = getattr(monster, kind.title())
        self.monsters.append(monster_class(surf, (x, y)))

    def __add_obstacle(self, kind=None, left=None):
        sprites = {
            'debris': 'debris',
            'meteor': 'meteor',
            'driller': 'driller-flying',
        }
        if kind is None:
            kind = 'debris'
            # kind = random.choice(sprites.keys())

        sprite = sprites[kind]
        surf, size = self.assets.images[sprite]

        if left is None:
            x = random.randint(20 + size[0], self.screen_size[0] - (20 + size[0]))
        else:
            x = left
        y = -50
        _class = getattr(obstacle, kind.title())
        self.monsters.append(_class(surf, (x, y)))


    def add_explosion(self, source, kind='default'):
        """
        Add an explosion to the screen.
        Source must have a .rect attribute.
        """
        image_name = {
            # kind: asset (name attrib, or file)
            'default': 'explode',
            'hero': 'explode',  # TODO: Alternative explosions
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

    def set_level(self, lvl):
        self.stage_clear = False
        self.level = lvl
        # Make a copy so we don't pop waves out of our original level
        self.waves = list(lvl.waves)

    def remove_dead_objects(self):
        """ Update our contents to drop dead or completed objects. """
        self.bullets = [b for b in self.bullets if not b.dead]
        self.bombs = [b for b in self.bombs if not b.dead]
        self.explosions = [e for e in self.explosions if not e.complete]
        self.monsters = [m for m in self.monsters if not m.dead]

    def add_new_objects(self, time):
        """ Add monsters or whatever. """
        if self.waves:
            wave = self.waves[0]
            if time > wave[0]:
                for x in wave[1]:
                    self.__add_monster(kind=wave[2], left=x)
                self.waves.pop(0)  # Get rid of completed wave
                self.last_add = time  # Don't add randomly right after

        self.add_count = (self.add_count + 1) % self.add_monster_trigger
        if self.add_count == self.add_monster_trigger - 1:
            if random.random() > 0.4:
                self.__add_obstacle()
            else:
                self.__add_monster()

    def update(self, level_time):
        """ Once per frame, update all the world's objects. """
        self.remove_dead_objects()
        self.add_new_objects(level_time)

        if self.hero.dead:
            if not self.hero.exploded:
                self.hero.exploded = True
                self.add_explosion(self.hero, kind='hero')
        if self.hero.shooting:
            self.hero_shoot()

        if True in self.hero.lateral_firing.values():
            self.hero_fire_laterally()

        if self.hero.bomb_dropping:
            self.hero_drop_bomb()

        self.background.update()

        self.hero.update()

        self.antigrav.update(self.hero.rect.midbottom)

        for b in self.bullets:
            b.update()

        for b in self.bombs:
            b.update()

        for m in self.monsters:
            m.update()

        for e in self.explosions:
            e.update()

        # Infection goes down slowly over time
        self.infection = max(0, self.infection - 0.01)

    def hero_shoot(self):
        # Limit firing rate, should be done by hero?
        if 'reloading' not in self.hero.status:
            self.hero.set_status('reloading', 10)  # Limit firing rate
            self.assets.sounds['shot'].play()
            self.bullets.append(bullet.Bullet(self.hero, direction='up'))
            self.stats['bullets_fired'] += 1

    def hero_fire_laterally(self):
        for direction, active in self.hero.lateral_firing.items():
            if active:
                self.hero.lateral_firing[direction] = False
                self.assets.sounds['shot'].play()
                self.bullets.append(bullet.Bullet(self.hero, direction=direction))
                self.stats['bullets_fired'] += 1

    def hero_drop_bomb(self):
        self.assets.sounds['bomb-drop'].play()
        self.hero.bomb_dropping = False
        surf, size = self.assets.images['mine']
        self.bombs.append(bomb.Bomb(surf, self.hero))
        self.stats['bombs_dropped'] += 1

