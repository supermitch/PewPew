from base import BaseScene
from screens.worlds import VictoryWorld


class VictoryScene(BaseScene):
    """ You won the game scene. """

    def __init__(self, renderer):
        self.renderer = renderer
        super(VictoryScene, self).__init__(self.renderer.surf, self.renderer.fps)
        self.surfaces = VictoryWorld(self.surf.get_size()).surfaces

