import pygame

class BaseScene(object):
    """ Base Scene class with basic run, update and render methods. """
    def __init__(self, win_surf, FPS):
        self.surf = win_surf
        self.width, self.height = self.surf.get_size()
        self.FPS = FPS
        self.surfaces = []
        self.clock = pygame.time.Clock()

    def update(self):
        pass

    def run(self):
        while True:
            action = self.handle_events()
            if action:
                return action

            self.update()
            self.render()

            self.clock.tick(self.FPS)

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
