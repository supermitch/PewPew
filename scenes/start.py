import pygame
from pygame.locals import *

from screens.start import StartWorld
from screens.start import VictoryWorld

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


class StartScene(BaseScene):
    """ Game intro screen. """

    def __init__(self, win_surf, FPS):
        super(StartScene, self).__init__(win_surf, FPS)
        self.surf = win_surf
        self.width, self.height = self.surf.get_size()
        self.FPS = FPS
        self.surfaces = StartWorld(self.surf.get_size()).surfaces

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'quit'
                elif event.key == K_SPACE:
                    return 'continue'

class VictoryScene(BaseScene):
    """ You won the game scene. """

    def __init__(self, win_surf, FPS):
        super(VictoryScene, self).__init__(win_surf, FPS)
        self.surf = win_surf
        self.width, self.height = self.surf.get_size()
        self.FPS = FPS
        self.surfaces = VictoryWorld(self.surf.get_size()).surfaces

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            elif event.type == KEYDOWN:
                if event.key in (K_ESCAPE, K_n):
                    return 'quit'
                elif event.key in (K_SPACE, K_y):
                    return 'continue'

