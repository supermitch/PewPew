#!/usr/bin/env python
from __future__ import division
import argparse
import random
import sys

import pygame
from pygame.locals import *
from pygame import Color

from classes import (collider, level, world, renderer, assetloader)

from scenes.scenes import StartScene, VictoryScene, GameOverScene
from screens.level import LevelScreen


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', type=int, default=1,
                        help='Starting level (default 1)')
    args = parser.parse_args()
    return args


class PewPew(object):
    """ Primary game object """

    def __init__(self, level, width=800, height=600):
        """ Initalize some game constants """
        self.current_level = level
        self.FPS = 60

        self.W_WIDTH = width
        self.W_HEIGHT = height
        self.screen_size = (self.W_WIDTH, self.W_HEIGHT)

        self.renderer = renderer.Renderer(self.screen_size)
        self.assets = assetloader.AssetLoader()
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
        """ Run the actual game """

        # Display start screen
        start_scene = StartScene(self.renderer.surf, self.FPS)
        start_scene.run()

        # Display the main game screen
        game_scene = GameScene(self.renderer.surf, self.FPS)
        game_scene.set_level(self.current_level - 1)
        result = game_scene.run()

        if result in ('infected', 'died'):
            gameover_scene = GameOverScene(self.renderer.surf, self.FPS)
            return gameover_scene.run()
        else:
            victory_scene = VictoryScene(self.renderer.surf, self.FPS)
            return victory_scene.run()


def terminate():
    """ Shut 'er down. """
    pygame.quit()  # uninitialize
    sys.exit('Thanks for playing!')


def main():
    """ Run the game. """
    args = setup_args()

    print('Initalizing PyGame...')
    pygame.init()  # Initialize pygame
    print('Done.')

    while True:
        app = PewPew(level=args.level)  # Instantiate new app
        result = app.run()

        if result == 'quit':
            terminate()
        elif result == 'continue':
            continue

if __name__ == "__main__":
    main()

