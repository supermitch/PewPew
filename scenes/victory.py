from .base import BaseScene

class VictoryScene(BaseScene):
    """ You won the game scene. """

    def __init__(self, win_surf, FPS):
        super(VictoryScene, self).__init__(win_surf, FPS)
        self.surfaces = VictoryWorld(self.surf.get_size()).surfaces

