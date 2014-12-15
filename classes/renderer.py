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
            pygame.draw.rect(self.surf, *bullet.draw())

        # Text displays
        self.plot_stats(self.world.stats)

        return None


    def plot_stats(self, stats):
        """ Plots text statistics, but doesn't display them. """
        left = 20

        try:
            accuracy = float(stats['bullets_hit']) / stats['bullets_fired'] * 100
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

    def plot_fps(self, fps):
        surf = self.text.render('FPS: {:.1f}'.format(fps), True, self.text_colour,
                                self.BG_COLOR)
        self.surf.blit(surf, (20, 160))

