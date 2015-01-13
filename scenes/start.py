import pygame
from pygame.locals import *

from screens.start import StartScreen

class StartScene(object):
    """ Game intro screen. """

    def __init__(self, win_surf, FPS):
        # TODO: Do we need a clock in the screen?
        self.surf = win_surf
        self.width, self.height = self.surf.get_size()
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.surfaces = StartScreen().surfaces

    def run(self):
        while True:
            action = self.handle_events()
            if action:
                return action

            self.update()
            self.render()

            self.clock.tick(self.FPS)

    def update(self):
        pass

    def render(self):
        self.surf.fill(pygame.Colors('black'))
        for surf, pos in self.surfaces:
            self.surf.blit(surf, pos)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'quit'
                elif event.key == K_SPACE:
                    return 'play'



