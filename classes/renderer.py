from __future__ import division
import math

import pygame
from pygame.locals import *
from pygame import Color

class Renderer(object):
    """ Render the world. """

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.surf = pygame.display.set_mode(self.screen_size, RESIZABLE)
        self.fps = 60
        pygame.display.set_caption('Pew Pew 1.0')
        self.BG_COLOR = (10, 10, 10)

        self.text = pygame.font.Font(None, 16)
        self.normal_text = pygame.font.Font(None, 30)
        self.text_colour = (200, 200, 255)


    def render(self):
        # Start with a blank screen
        self.surf.fill(self.BG_COLOR)

        self.surf.blit(*self.world.background.draw())

        if not self.world.hero.dead:
            if self.world.hero.thrusters['grav']:
                surf, pos = self.world.antigrav.draw()
                self.surf.blit(surf, pos)

            if 'injured' in self.world.hero.status:
                surf, pos = self.world.hero.draw()
                surf = surf.copy()  # Don't modify original
                # Add red overlay
                surf.fill((255, 0, 0), special_flags=BLEND_RGB_ADD)
                self.surf.blit(surf, pos)
            else:
                self.surf.blit(*self.world.hero.draw())

        for monster in self.world.monsters:
            surf, pos = monster.draw()
            if 'injured' in monster.status:
                surf = surf.copy()  # Don't modify original
                # Add red overlay
                surf.fill((255, 0, 0), special_flags=BLEND_RGB_ADD)
            if hasattr(monster, 'rotation'):
                degrees = math.degrees(monster.theta)
                width, height = surf.get_size()
                surf = pygame.transform.rotate(surf, degrees)
                new_width, new_height = surf.get_size()
                x, y = pos
                new_x = x - (new_width/2.0 - width/2.0)
                new_y = y - (new_height/2.0 - height/2.0)
                pos = new_x, new_y
            self.surf.blit(surf, pos)

        for explosion in self.world.explosions:
            self.surf.blit(*explosion.draw())

        for bullet in self.world.bullets:
            self.surf.blit(*bullet.draw())

        self.surf.blit(self.world.assets.images['biohazard'][0], (617, 60))
        self.surf.blit(self.world.assets.images['heart'][0], (667, 60))
        self.surf.blit(self.world.assets.images['fuel'][0], (717, 60))

        self.surf.blit(*self.health_meter(self.world.hero.health_percentage))
        self.surf.blit(*self.fuel_meter(self.world.hero.fuel_percentage))
        self.surf.blit(*self.infection_meter(self.world.infection))

        # Text displays
        self.plot_stats(self.world.stats)

        # Show stage start message
        if self.world.stage_start:
            self.stage_start(self.world.level.number)

        # Show stage clear message
        if self.world.stage_clear:
            self.stage_clear(self.world.level.number)

        pygame.display.flip()


    def health_meter(self, health):
        """ Display our health meter. """
        health = min(100, health)  # For the sake of life meter, cap it?
        # Add a block for each 10 % of life remaining
        block_count = int(math.ceil(health/10.0))

        images = self.world.assets.images  # save typing
        frame, frame_size = images['meter_frame']
        surf = frame.copy()  # Don't blit onto original frame
        block, block_size = images['health_block']
        for i in range(block_count):
            y = frame_size[1] - 4 - block_size[1] - (i * (block_size[1] - 2))
            surf.blit(block, (4, y))
        pos = (670, 100)
        return surf, pos

    def fuel_meter(self, fuel):
        """ Display our health meter. """
        fuel = min(100, fuel)  # For the sake of meter, cap it
        # Add a block for each 10 % of life remaining
        block_count = int(math.ceil(fuel/10.0))

        images = self.world.assets.images  # save typing

        frame, frame_size = images['meter_frame']
        surf = frame.copy()  # Don't blit onto original frame
        block, block_size = images['health_block']
        # Adjust color for fuel meter
        block = block.copy()
        block.fill((150, 200, 50), special_flags=BLEND_RGB_MULT)
        for i in range(block_count):
            y = frame_size[1] - 4 - block_size[1] - (i * (block_size[1] - 2))
            surf.blit(block, (4, y))
        pos = (720, 100)
        return surf, pos

    def infection_meter(self, infection):
        """ Display our infection meter. """
        infection = min(100, infection)  # For the sake of meter, cap it
        # Add a block for each 10 % of life remaining
        block_count = int(math.ceil(infection/10.0))

        images = self.world.assets.images  # save typing

        frame, frame_size = images['meter_frame']
        surf = frame.copy()  # Don't blit onto original frame
        block, block_size = images['health_block']
        # Adjust color for fuel meter
        block = block.copy()
        block.fill((255, 0, 0), special_flags=BLEND_RGB_ADD)
        for i in range(block_count):
            y = frame_size[1] - 4 - block_size[1] - (i * (block_size[1] - 2))
            surf.blit(block, (4, y))
        pos = (620, 100)
        return surf, pos


    def plot_stats(self, stats):
        """ Plots text statistics, but doesn't display them. """
        left = 20

        try:
            accuracy = float(stats['bullets_hit']) / stats['bullets_fired']
        except ZeroDivisionError:
            accuracy = 0.0

        strings = [
            'Accuracy: {:.2%}'.format(accuracy),
            'Enemies killed: {}'.format(stats['monsters_killed']),
            'Enemies missed: {}'.format(stats['monsters_missed']),
        ]
        for y, string in zip(range(40, 81, 20), strings):
            surf = self.text.render(string, True, self.text_colour,
                                    self.BG_COLOR)
            self.surf.blit(surf, (left, y))

        surf = self.text.render('FPS: {:.1f}'.format(stats['fps']), True,
                                self.text_colour, self.BG_COLOR)
        self.surf.blit(surf, (20, 160))

    def stage_start(self, stage):
        """ Display a 'stage start' message overlay. """
        surf = self.normal_text.render('Wave {} inbound!'.format(stage),
                                       True, Color('ivory'))
        self.surf.blit(surf, (300, 250))

    def stage_clear(self, stage):
        """ Display a 'stage clear' message overlay. """
        surf = self.normal_text.render('Stage {} cleared!'.format(stage),
                                       True, Color('ivory'))
        self.surf.blit(surf, (300, 250))

