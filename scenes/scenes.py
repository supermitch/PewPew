import pygame
from pygame.locals import *

from screens.worlds import StartWorld, VictoryWorld, GameOverWorld

class BaseScene(object):
    """ Base Scene class with basic run, update and render methods. """
    def __init__(self, win_surf, FPS):
        self.surf = win_surf
        self.width, self.height = self.surf.get_size()
        self.FPS = FPS
        self.surfaces = []

    def update(self):
        pass

    def run(self):
        clock = pygame.time.Clock()
        while True:
            action = self.handle_events()
            if action:
                return action

            self.update()
            self.render()

            clock.tick(self.FPS)

    def render(self):
        self.surf.fill(pygame.Color('black'))
        for surf, pos in self.surfaces:
            self.surf.blit(surf, pos)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            elif event.type == KEYDOWN:
                if event.key in (K_ESCAPE, K_n):
                    return 'quit'
                elif event.key in (K_SPACE, K_y):
                    return 'continue'


class StartScene(BaseScene):
    """ Game intro screen. """

    def __init__(self, win_surf, FPS):
        super(StartScene, self).__init__(win_surf, FPS)
        self.surfaces = StartWorld(self.surf.get_size()).surfaces

class VictoryScene(BaseScene):
    """ You won the game scene. """

    def __init__(self, win_surf, FPS):
        super(VictoryScene, self).__init__(win_surf, FPS)
        self.surfaces = VictoryWorld(self.surf.get_size()).surfaces

class GameOverScene(BaseScene):
    """ You died, or planet was infected. Game over. """

    def __init__(self, win_surf, FPS):
        super(GameOverScene, self).__init__(win_surf, FPS)
        self.surfaces = GameOverWorld(self.surf.get_size()).surfaces

