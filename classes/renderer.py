from __future__ import division
import math

import numpy
import pygame
from pygame.locals import *

def color_surface(surface, red, green, blue):
    """ Modify R, G or B channels to new values. """
    arr = pygame.surfarray.pixels3d(surface)
    arr[:, :, 0] = red
    arr[:, :, 1] = green
    arr[:, :, 2] = blue

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
            if 'injured' in self.world.hero.status:
                surf, pos = self.world.hero.draw()
                # don't fuck up original image
                surf = surf.copy()
                # Add red overlay
                surf.fill((255, 0, 0), special_flags=BLEND_RGB_ADD)
                self.surf.blit(surf, pos)
            else:
                self.surf.blit(*self.world.hero.draw())

        for monster in self.world.monsters:
            if 'injured' in monster.status:
                # Get original monster surface
                surf, pos = monster.draw()
                # don't fuck up original image
                surf = surf.copy()
                # Add red overlay
                surf.fill((255, 0, 0), special_flags=BLEND_RGB_ADD)
                # Now blit the result
                self.surf.blit(surf, pos)
            else:
                self.surf.blit(*monster.draw())

        for explosion in self.world.explosions:
            self.surf.blit(*explosion.draw())

        for bullet in self.world.bullets:
            # Bullets are filled rects, for now.
            self.surf.blit(*bullet.draw())

        self.surf.blit(*self.health_meter(self.world.hero.health_percentage))
        # Text displays
        self.plot_stats(self.world.stats)

        pygame.display.flip()

        return None

    def health_meter(self, health):
        """ Display our health meter. """

        images = self.world.assets.images  # save typing

        health = min(100, health)  # For the sake of life meter, cap it?

        frame, frame_size = images['meter_frame']
        surf = frame.copy()  # Don't blit onto original frame
        block, block_size = images['health_block']
        block_count = int(math.ceil(health/10.0))
        # Add a block for each 10 % of life remaining
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

        # === FUEL stats
        surf = self.text.render("Fuel remaining: %0.2f" % self.world.hero.fuel,
                                True, self.text_colour, self.BG_COLOR)
        self.surf.blit(surf, (left, 100))

        # === HEALTH info
        surf = self.text.render('Remaining: %0.2f' % self.world.hero.health,
                                True, self.text_colour, self.BG_COLOR)
        self.surf.blit(surf, (left, 140))

        surf = self.text.render('FPS: {:.1f}'.format(stats['fps']), True, self.text_colour,
                                self.BG_COLOR)
        self.surf.blit(surf, (20, 160))

