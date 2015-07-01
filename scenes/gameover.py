from . import BaseScene

class GameOverScene(BaseScene):
    """ You died, or planet was infected. Game over. """

    def __init__(self, win_surf, FPS):
        super(GameOverScene, self).__init__(win_surf, FPS)
        self.surfaces = GameOverWorld(self.surf.get_size()).surfaces

