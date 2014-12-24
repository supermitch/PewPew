#!/usr/bin/env python
from __future__ import division
import random
import sys

import pygame
from pygame.locals import *
from pygame import Color

from classes import collider
from classes import hero
from classes import monster
from classes import bullet
from classes import wall
from classes import explosion
from classes import world
from classes import renderer
from classes import assetloader

from screens.start import StartScreen
from screens.level import LevelScreen


class PewPew(object):
    """ Primary game object. Not sure this is the best way,
    saw it in someone's game... """

    def __init__(self):
        """Initalize some game constants."""

        self.FPS = 60

        self.W_WIDTH = 800
        self.W_HEIGHT = 600
        self.screen_size = (self.W_WIDTH, self.W_HEIGHT)

        self.renderer = renderer.Renderer(self.screen_size)
        self.assets = assetloader.AssetLoader()
        self.world = world.World(self.screen_size, self.assets)
        self.renderer.world = self.world
        self.collider = collider.Collider(self.world)

        self.stats = {
            'fps': self.FPS,
            'bullets_fired': 0,
            'bullets_hit': 0,
            'monsters_killed': 0,
            'monsters_missed': 0,
            'score': 0,
        }
        self.world.stats = self.stats

    def run(self):
        """Run the actual game."""

        # Initialize framerate clock
        clock = pygame.time.Clock()

        # Display Start Screen
        start_screen = StartScreen(self.renderer.surf, clock, self.FPS)
        start_screen.render()
        del start_screen

        #Display Level 1 Screen
        level_screen = LevelScreen(1, self.renderer.surf, clock, self.FPS)
        level_screen.render()
        del level_screen

        time_of_death = None
        start_time = pygame.time.get_ticks() / 1000
        while True:  # Game loop

            time = (pygame.time.get_ticks() / 1000) - start_time
            # TODO: Remove some day
            self.stats['fps'] = clock.get_fps()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key in (K_q, K_ESCAPE):
                        terminate()
                    elif event.key == K_p:
                        self.pause_game()
                    elif event.key == K_x:
                        self.world.hero.self_destruct()
                    elif event.key in (K_h, K_LEFT):
                        self.world.hero.activate_thrusters('left')
                    elif event.key in (K_l, K_RIGHT):
                        self.world.hero.activate_thrusters('right')
                    elif event.key == K_SPACE:
                        self.world.hero_shoot()
                elif event.type == KEYUP:
                    if event.key in (K_h, K_LEFT):
                        self.world.hero.activate_thrusters('left', False)
                    elif event.key in (K_l, K_RIGHT):
                        self.world.hero.activate_thrusters('right', False)
                    elif event.key == K_UP:
                        pass
                    elif event.key == K_DOWN:
                        pass

            self.world.update(time)

            self.collider.update()

            if self.world.hero.dead:
                if time_of_death is None:
                    time_of_death = time
                else:
                    if time - time_of_death > 2:
                        break # out of game loop

            self.renderer.render()

            clock.tick(self.FPS)

        return 'dead'


    def pause_game(self):
        """ Pauses the game. """

        # Semi-transparent background
        s = pygame.Surface(self.renderer.surf.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.renderer.surf.blit(s, (0, 0))

        text = pygame.font.Font(None, 60)
        surf = text.render("Paused!", True, Color('cornflowerblue'))
        self.renderer.surf.blit(surf, (self.W_WIDTH/2 - surf.get_width()/2,
                                  self.W_HEIGHT/2 - surf.get_height()/2))
        small_text = pygame.font.Font(None, 30)
        surf = small_text.render("(Press spacebar to resume)", True, Color('ivory'))
        self.renderer.surf.blit(surf, (self.W_WIDTH/2 - surf.get_width()/2,
                                  self.W_HEIGHT/2 - surf.get_height()/2 + 60))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key in [K_ESCAPE, K_q]:
                        terminate()
                    elif event.key == K_SPACE:
                        return True

    def game_over(self):
        """ Game over scene. """
        center_x = self.W_WIDTH / 2
        center_y = self.W_HEIGHT / 2

        # Semi-transparent background
        s = pygame.Surface(self.renderer.surf.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.renderer.surf.blit(s, (0, 0))

        text = pygame.font.Font(None, 60)
        surf = text.render("Game Over!", True, Color('firebrick'))
        pos = (center_x - surf.get_width()/2, center_y - surf.get_height()/2)
        self.renderer.surf.blit(surf, pos)

        small_text = pygame.font.Font(None, 30)
        surf = small_text.render("Play again?", True, Color('ivory'))
        pos = (center_x - surf.get_width()/2, center_y - surf.get_height()/2 + 60)
        self.renderer.surf.blit(surf, pos)

        surf = small_text.render("(Y)es         (N)o", True, Color('ivory'))
        pos = (center_x - surf.get_width()/2, center_y - surf.get_height()/2+ 100)
        self.renderer.surf.blit(surf, pos)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()
                    elif event.key in [K_SPACE, K_y]:
                        return True
                    elif event.key in [K_n]:
                        return False
        return False


def terminate():
    """ Shut 'er down. """
    pygame.quit()   # uninitialize
    sys.exit("Thanks for playing!")

def main():
    """ Run the game. """
    while True:
        pygame.init()   # Initialize pygame
        app = PewPew()  # Instantiate new app
        result = app.run()
        if result == 'dead':
            if app.game_over():  #  Prompt to continue
                continue
            else:
                terminate()

if __name__ == "__main__":
    main()

