import pygame
from pygame.locals import *

class LevelScreen(object):
    """ Intro screen to each Level. """

    def __init__(self, level, win_surf, fps_clock, FPS):
        # TODO: Do we need a clock in the screen?
        self.level = level
        self.win_surf = win_surf
        self.win_width, self.win_height = self.win_surf.get_size()
        self.fps_clock = fps_clock
        self.FPS = FPS

    def render(self):
        # TODO: This is all very ugly
        black = (0, 0, 0)
        self.win_surf.fill(black)
        font = pygame.font.Font(None, 60)
        color = (250, 250 ,255)
        text = 'Level {}'.format(self.level)
        surf = font.render(text, True, color)
        self.win_surf.blit(surf, (self.win_width/2 - surf.get_width()/2,
                           self.win_height/2 - surf.get_height()/2))
        small_font = pygame.font.Font(None, 30)
        color = (255, 255, 255)
        text = 'Ready. Set. Pew!'
        surf = small_font.render(text, True, color)
        self.win_surf.blit(surf, (self.win_width/2 - surf.get_width()/2,
                           self.win_height/2 - surf.get_height()/2 + 60))
        pygame.display.update()

        # TODO: Event handler shouldn't be in screen?
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_SPACE:
                        return None
            self.fps_clock.tick(self.FPS)


