from __future__ import division
import math

import pygame
from pygame.locals import *

class Renderer(object):
    """ Render the world. """

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.surf = pygame.display.set_mode(self.screen_size, RESIZABLE)
        pygame.display.set_caption('Pew Pew 1.0')
        self.BG_COLOR = (10, 10, 10)

        self.text = pygame.font.Font(None, 16)
        self.text_colour = (200, 200, 255)


    def render(self):
        # Start with a blank screen
        self.surf.fill(self.BG_COLOR)

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
            if 'injured' in monster.status:
                surf, pos = monster.draw()
                surf = surf.copy()  # Don't modify original
                # Add red overlay
                surf.fill((255, 0, 0), special_flags=BLEND_RGB_ADD)
                self.surf.blit(surf, pos)
            else:
                self.surf.blit(*monster.draw())

        for explosion in self.world.explosions:
            self.surf.blit(*explosion.draw())

        for bullet in self.world.bullets:
            self.surf.blit(*bullet.draw())

        self.surf.blit(*self.health_meter(self.world.hero.health_percentage))
        self.surf.blit(*self.fuel_meter(self.world.hero.fuel_percentage))

        # Text displays
        self.plot_stats(self.world.stats)

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

