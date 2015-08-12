from base import BaseScene
from screens.worlds import GameOverWorld

class GameOverScene(BaseScene):
    """ You died, or planet was infected. Game over. """

    def __init__(self, renderer, result):
        self.renderer = renderer
        super(GameOverScene, self).__init__(self.renderer.surf, self.renderer.fps)
        self.surfaces = GameOverWorld(self.surf.get_size(), result).surfaces

