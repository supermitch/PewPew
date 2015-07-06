#!/usr/bin/env python
from __future__ import division
import argparse
import random
import sys

import pygame

from classes import renderer
from scenes import StartScene, GameScene, VictoryScene, GameOverScene


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', type=int, default=1, help='Starting level (default 1)')
    return parser.parse_args()


class PewPew(object):
    """ Primary game object """

    def __init__(self):
        screen_size = (800, 600)
        self.renderer = renderer.Renderer(screen_size)

    def run(self, level):
        """ Run the actual game """
        while True:
            if self.play(level) == 'quit':
                return

    def play(self, level):
        # Display intro screen
        start_scene = StartScene(self.renderer)
        start_scene.run()

        # Display the main game screen
        game_scene = GameScene(self.renderer)
        game_scene.set_level(level - 1)
        result = game_scene.run()

        if result in ('infected', 'died'):
            gameover_scene = GameOverScene(self.renderer)
            return gameover_scene.run()
        elif result in ('victory'):
            victory_scene = VictoryScene(self.renderer)
            return victory_scene.run()
        else:
            return result


def main():
    """ Run the game. """
    args = setup_args()

    print('Initalizing PyGame... please wait.')
    pygame.init()  # Initialize pygame

    app = PewPew()
    app.run(level=args.level)

    pygame.quit()  # Uninitialize
    sys.exit('Thanks for playing!')


if __name__ == "__main__":
    main()

