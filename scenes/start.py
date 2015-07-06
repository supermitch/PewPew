from base import BaseScene

class StartScene(BaseScene):
    """ Game intro screen. """

    def __init__(self, renderer):
        self.renderer = renderer
        super(StartScene, self).__init__(self.renderer.surf, self.renderer.fps)

        self.surfaces = StartWorld(self.surf.get_size()).surfaces

