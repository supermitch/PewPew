#!/usr/bin/env python
import random
import sys

import pygame
from pygame.locals import *

from classes import collider
from classes import ship
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
        pygame.init()   # initialize pygame

        self.FPS = 60

        self.W_WIDTH = 800
        self.W_HEIGHT = 600
        self.screen_size = (self.W_WIDTH, self.W_HEIGHT)

        self.renderer = renderer.Renderer(self.screen_size)
        self.assets = assetloader.AssetLoader()
        self.world = world.World(self.screen_size, self.assets)
        self.renderer.world = self.world
        self.collider = collider.Collider(self.world)

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

        self.world.stats = {
            'fps': self.FPS,
            'bullets_fired': 0,
            'bullets_hit': 0,
            'monsters_killed': 0,
            'monsters_missed': 0,
        }

        while True:  # Game loop

            time = pygame.time.get_ticks()
            self.world.stats['fps'] = clock.get_fps()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key in (K_q, K_ESCAPE):
                        self.terminate()
                    elif event.key == K_p:
                        self.pause_game()
                    elif event.key == K_x:  # Reset
                        self.game_over()
                    elif event.key in (K_h, K_LEFT):
                        self.world.hero.activate_thrusters('left')
                    elif event.key in (K_l, K_RIGHT):
                        self.world.hero.activate_thrusters('right')
                    elif event.key == K_SPACE:
                        self.world.hero_shoot()
                elif event.type == KEYUP:
                    if event.key in (K_h, K_LEFT):
                        self.world.hero.activate_thrusters('off')
                    elif event.key in (K_l, K_RIGHT):
                        self.world.hero.activate_thrusters('off')
                    elif event.key == K_UP:
                        pass
                    elif event.key == K_DOWN:
                        pass

            self.world.update(time)

            self.collider.update()

            if self.world.hero.dead:
                break # out of game loop

            self.renderer.render()

            clock.tick(self.FPS)

        if self.world.hero.death:
            self.game_over()


    def game_over(self):
        print("Game over!")
        print("Do you want to play again? (y/n)")
        waiting_for_answer = True
        while waiting_for_answer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key in (K_ESCAPE, K_q):
                        self.terminate()
                    elif event.key == K_n:
                        self.terminate()
                    elif event.key == K_y:
                        waiting_for_answer = False
        self.run()  # Recursion idiocy here.

    def pause_game(self):
        print('paused!')

        text = pygame.font.Font(None, 60)
        surf = text.render("Paused!", True, (0,0,255))
        self.win_surf.blit(surf, (self.W_WIDTH/2 - surf.get_width()/2,
                                  self.W_HEIGHT/2 - surf.get_height()/2))
        small_text = pygame.font.Font(None, 30)
        surf = small_text.render("(Press spacebar to resume)", True, (0,0,255))
        self.win_surf.blit(surf, (self.W_WIDTH/2 - surf.get_width()/2,
                                  self.W_HEIGHT/2 - surf.get_height()/2 + 60))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key in (K_ESCAPE, K_q):
                        self.terminate()
                    elif event.key == K_SPACE:
                        break
        return False

    def terminate(self):
        """ Shut 'er down. """
        pygame.quit()   # uninitialize
        sys.exit()


if __name__ == "__main__":
    app = PewPew()  # Instantiate new app
    app.run()

